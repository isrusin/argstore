"""Command-line parsing module with support of metadata dumping

This is argparse extension for dumping of execution options
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


class ArgumentParser(_ArgumentParser):
    """Argument parser class.

    Replacement (and extension) of the argparse.ArgumentParser class
    that stores additional info during argument specification to format
    the output metadata.
    """

    def __init__(self, **kwargs):
        super(ArgumentParser, self).__init__(**kwargs)
        self._metadata_strs = []

    def add_argument(self, metamsg="{}", **kwargs):
        self._metadata_strs.append(metamsg)
        super(ArgumentParser, self).add_argument(**kwargs)

    def add_argument_group(self, metamsg="{}", **kwargs):
        self._metadata_strs.append(metamsg)
        super(ArgumentParser, self).add_argument_group(**kwargs)

