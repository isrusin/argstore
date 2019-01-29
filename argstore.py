"""Command-line parsing module with support of argument dumping

This is argparse wrapping which keeps execution options and arguments
and writes them to the output text files.
"""

__version__ = "0.1"
__all__ = [] # filled out later


import sys

from argparse import ArgumentParser as _ArgumentParser
from argparse import (Action, ArgumentDefaultsHelpFormatter,
    ArgumentError, ArgumentTypeError, FileType,
    HelpFormatter, MetavarTypeHelpFormatter, Namespace,
    RawDescriptionHelpFormatter, RawTextHelpFormatter,
    ONE_OR_MORE, OPTIONAL, PARSER, REMAINDER,
    SUPPRESS, ZERO_OR_MORE
)


class ArgumentContainerWrapper(object):
    """Root wrapper of the argument containers."""

    meta_tag = ""
    meta_title = "\n"
    meta_desc = "\n"
    meta_epilog = "\n"
    meta_args = None
    meta_groups = None
    meta_formatters = None

    def __init__(self, subj, meta_tag=None, meta_title=None,
                 meta_desc=None, meta_epilog=None, meta_args=None,
                 meta_groups=None, meta_formatters=None):
        self.subj = subj
        self._updattr("meta_tag", meta_tag)
        self._updattr("meta_title", meta_title)
        self._updattr("meta_desc", meta_desc)
        self._updattr("meta_epilog", meta_epilog)
        self._updattr("meta_args", meta_args, [])
        self._updattr("meta_groups", meta_groups, [])
        self._updattr("meta_formatters", meta_formatters, {})

    def add_argument(self, *args, meta_name=None, meta_str=None,
                     meta_formatter=None, **kwargs):
        _argument = self.subj.add_argument(*args, **kwargs)
        if meta_formatter is None and meta_str is None:
            if isinstance(_argument.type, FileType):
                meta_formatter = lambda val: val.name
        arg_dest = _argument.dest
        self.meta_formatters[arg_dest] = meta_formatter
        if meta_str is None:
            if meta_name is None:
                meta_name = arg_dest
            meta_str = " %s: {%s}\n" % (meta_name, arg_dest)
        self.meta_args.append(meta_str)
        return _argument

    def add_argument_group(self, *args, meta_tag=None, meta_title=None,
                           meta_name=None, meta_desc=None,
                           meta_epilog=None, **kwargs):
        _group = self.subj.add_argument_group(*args, **kwargs)
        if meta_title is None:
            if meta_name is None:
                meta_name = _group.title or ""
            meta_title = "\n --- %s ---\n" % meta_name
        group = ArgumentGroup(
            _group, meta_tag=meta_tag, meta_title=meta_title,
            meta_desc=meta_desc, meta_epilog=meta_epilog
        )
        self.meta_groups.append(group)
        return group

    def _updattr(self, name, value, default=None):
        if value is None:
            try:
                value = self.__getattribute__(name)
            except AttributeError:
                pass
        if value is None:
            value = default
        self.__setattr__(name, value)

    def prepare_template(self):
        template_strs = [
            self.meta_title, self.meta_desc, *self.meta_args,
        ]
        for group in self.meta_groups:
            group_strs = group.prepare_template().splitlines(True)
            template_strs.extend(group_strs)
        template_strs.append(self.meta_epilog)
        template_strs = ["", *(i for i in template_strs if i)]
        return self.meta_tag.join(template_strs)

    def prepare_values(self, args):
        formatters = self.meta_formatters.copy()
        for group in self.meta_groups:
            formatters.update(group.meta_formatters)
        values = dict.fromkeys(formatters, "<empty>")
        for key, value in vars(args).items():
            formatter = formatters[key]
            if formatter is not None:
                values[key] = formatter(value)
            else:
                values[key] = value
        return values


class ArgumentParser(ArgumentContainerWrapper):
    """Argument parser class.

    Replacement of the argparse.ArgumentParser that wraps it and
    stores metadata during argument addition.
    """

    meta_tag = "##"

    def __init__(self, *args, meta_tag=None, meta_title=None,
                 meta_desc=None, meta_epilog=None, **kwargs):
        subj = _ArgumentParser(*args, **kwargs)
        if meta_title is None:
            meta_title = "### %s\n" % (subj.prog or sys.argv[0])
        super().__init__(
            subj, meta_tag=meta_tag, meta_title=meta_title,
            meta_desc=meta_desc, meta_epilog=meta_epilog
        )

    def parse_args(self, argv=None, namespace=None):
        template = self.prepare_template()
        args = self.subj.parse_args(argv, namespace)
        values = self.prepare_values(args)
        self.metadata = template.format(**values)
        return args


class ArgumentGroup(ArgumentContainerWrapper):

    meta_desc = ""
    meta_epilog = ""

