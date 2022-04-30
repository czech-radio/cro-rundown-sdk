# -*- coding: utf-8 -*-

"""
Test the project as a package e.g. check the version, style etc.
"""

from cro.rundown.sdk import __version__


def test_version():
    assert __version__ == "0.3.0"
