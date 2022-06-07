# -*- coding: utf-8  -*-

import io

import pytest


@pytest.mark.skip
@pytest.mark.service
def test_rundown_cleanse():
    assert False


@pytest.mark.skip
@pytest.mark.service
def test_rundown_compress():
    assert False


# Parser tests.
from cro.rundown.sdk import RundownParser


@pytest.fixture
def rundown():
    return io.StringIO(
        """\
        <


    """
    )


# Parser tests.
from cro.rundown.sdk import RundownParser


@pytest.fixture
def rundown():
    return io.StringIO(
        """\
        <
    """
    )


@pytest.mark.skip
@pytest.mark.service
def test_rundown_parse():
    assert False
