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


class TestArgumentContainerWrapper(object):
    def test_init_defaults(self):
        wrapper = argstore.ArgumentContainerWrapper(
            _ArgumentContainerStub()
        )
        assert wrapper.meta_tag is not None
        assert wrapper.meta_title is not None
        assert wrapper.meta_desc is not None
        assert wrapper.meta_epilog is not None
        assert wrapper.meta_args is not None
        assert wrapper.meta_groups is not None
        assert wrapper.meta_formatters is not None

    def test_init_meta_kwargs(self):
        meta_tag = "meta_tag"
        meta_title = "meta_title"
        meta_desc = "meta_desc"
        meta_epilog = "meta_epilog"
        meta_args = ["meta_args", ]
        meta_groups = ["meta_groups", ]
        meta_formatters = ["meta_formatters", ]
        wrapper = argstore.ArgumentContainerWrapper(
            _ArgumentContainerStub(),
            meta_tag=meta_tag,
            meta_title=meta_title,
            meta_desc=meta_desc,
            meta_epilog=meta_epilog,
            meta_args=meta_args,
            meta_groups=meta_groups,
            meta_formatters=meta_formatters
        )
        assert wrapper.meta_tag == meta_tag
        assert wrapper.meta_title == meta_title
        assert wrapper.meta_desc == meta_desc
        assert wrapper.meta_epilog == meta_epilog
        assert wrapper.meta_args is meta_args
        assert wrapper.meta_groups is meta_groups
        assert wrapper.meta_formatters is meta_formatters


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

