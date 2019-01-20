"""Command-line parsing module with support of metadata dumping

This is argparse wrapping for dumping of execution options
and argument values to the output files.
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


class ArgumentParser(object):
    """Argument parser class.

    Replacement of the argparse.ArgumentParser that wraps the class and
    stores additional info during argument specification to format the
    output metadata.
    """

    def __init__(self, *args, metatitle=None, metadesc=None, **kwargs):
        self.parser = _ArgumentParser(*args, **kwargs)
        self._meta_strs = []
        if metatitle is None:
            metatitle = "### %s\n" % (self.parser.prog or sys.argv[0])
        self._meta_strs.append(metatitle)
        if metadesc is None:
            metadesc = "\n"
        self._meta_strs.append(metadesc)

    def add_argument(self, *args, metamsg=None, **kwargs):
        _argument = self.parser.add_argument(*args, **kwargs)
        if metamsg is None:
            metamsg = " {%s}" % _argument.dest
        self._meta_strs.append(metamsg)
        return _argument

    def add_argument_group(self, *args, metamsg="{}", **kwargs):
        self._meta_strs.append(metamsg)
        return self.parser.add_argument_group(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        return self.parser(*args, **kwargs)

