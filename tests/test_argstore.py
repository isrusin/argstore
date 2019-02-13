"""Tests for argstore."""

import pytest
import sys

import argstore


class _ArgumentContainerStub(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def add_argument(self, *args, **kwargs):
        return args, kwargs

    def add_argument_group(self, *args, **kwargs):
        return _ArgumentContainerStub(*args, **kwargs)

    def add_mutually_exclusive_group(self, *args, **kwargs):
        return self.add_argument_group(*args, **kwargs)


def test_parser_creation_all_defaults():
    parser = argstore.ArgumentParser()
    assert parser.meta_tag is not None
    assert parser.meta_title is not None
    assert parser.meta_desc is not None
    assert parser.meta_epilog is not None
    assert parser.meta_args is not None
    assert parser.meta_groups is not None
    assert parser.meta_formatters is not None
    assert parser.subj is not None

def test_parser_parents_not_implemented():
    with pytest.raises(NotImplementedError):
        _parser = argstore.ArgumentParser(parents=[])

