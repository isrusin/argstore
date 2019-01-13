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

    def __init__(self, *args, **kwargs):
        self._metadata_strs = []
        self.parser = _ArgumentParser(*args, **kwargs)

    def add_argument(self, *args, metamsg="{}", **kwargs):
        self._metadata_strs.append(metamsg)
        return self.parser.add_argument(*args, **kwargs)

    def add_argument_group(self, *args, metamsg="{}", **kwargs):
        self._metadata_strs.append(metamsg)
        return self.parser.add_argument_group(*args, **kwargs)

