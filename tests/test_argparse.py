"""Tests for some required argparse features."""

import argparse
import sys


def test_parser_has_prog_attribute():
    parser = argparse.ArgumentParser()
    assert hasattr(parser, "prog")
    assert parser.prog is not None

def test_parser_fill_prog_attribute():
    parser = argparse.ArgumentParser(prog="test")
    assert hasattr(parser, "prog")
    assert parser.prog == "test"

def test_argument_has_dest():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument("-f")
    assert hasattr(arg, "dest")
    assert arg.dest

def test_argument_has_type():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument("-f", type=argparse.FileType("r"))
    assert hasattr(arg, "type")
    assert isinstance(arg.type, argparse.FileType)

