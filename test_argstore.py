#! /usr/bin/env python3

"""Tests for argstore."""

import sys

import argstore


def main():
    parser = argstore.ArgumentParser()
    args = parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())

