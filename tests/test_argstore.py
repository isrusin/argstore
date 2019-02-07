"""Tests for argstore."""

import sys

import argstore

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

