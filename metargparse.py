"""Command-line parsing module with support of argument dumping

This is argparse wrapping which keeps execution options and arguments
and writes them to the output text files.
"""

__version__ = "0.1"
__all__ = [] # filled out later


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

    meta_title = "\n"
    meta_desc = "\n"
    meta_epilog = "\n"
    meta_args = None
    meta_groups = None

    def __init__(self, subj, meta_title=None, meta_desc=None,
                 meta_epilog=None, meta_args=None, meta_groups=None):
        self.subj = subj
        self.meta_title = self._updattr("meta_title", meta_title)
        self.meta_desc = self._updattr("meta_desc", meta_desc)
        self.meta_epilog = self._updattr("meta_epilog", meta_epilog)
        self.meta_args = self._updattr("meta_args", meta_args, [])
        self.meta_groups = self._updattr("meta_groups", meta_groups, [])

    def add_argument(self, *args, meta_name=None, meta_str=None,
                     **kwargs):
        _argument = self.subj.add_argument(*args, **kwargs)
        if meta_str is None:
            if meta_name is None:
                meta_name = _argument.dest
            meta_str = " %s: {%s}\n" % (meta_name, _argument.dest)
        self.meta_args.append(meta_str)
        return _argument

    def add_argument_group(self, *args, meta_title=None, meta_name=None,
                           meta_desc=None, **kwargs):
        _group = self.subj.add_argument_group(*args, **kwargs)
        if meta_title is None:
            if meta_name is None:
                meta_name = _group.title or ""
            meta_title = " --- %s ---\n" % meta_name
        group = ArgumentContainerWrapper(
            _group, meta_title=meta_title, meta_desc=meta_desc
        )
        self.meta_groups.append(group)
        return group

    def _update_value(self, name, value, default=None):
        if value is None:
            try:
                value = self.__getattribute__(name)
            except AttributeError:
                pass
        if value is None:
            value = default
        self.__setattr__(name, value)


class ArgumentParser(ArgumentContainerWrapper):
    """Argument parser class.

    Replacement of the argparse.ArgumentParser that wraps it and
    stores metadata during argument addition.
    """

    def __init__(self, *args, meta_title=None, meta_desc=None,
                 meta_epilog=None, **kwargs):
        subj = _ArgumentParser(*args, **kwargs)
        if meta_title is None:
            meta_title = "### %s\n" % (subj.prog or sys.argv[0])
        super().__init__(
            subj, meta_title=meta_title, meta_desc=meta_desc,
            meta_epilog=meta_epilog
        )

    def parse_args(self, *args, **kwargs):
        return self.subj.parse_args(*args, **kwargs)

