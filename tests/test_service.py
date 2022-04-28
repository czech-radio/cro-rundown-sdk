# -*- coding: utf-8  -*-


import pytest



@pytest.mark.skip
@pytest.mark.service
def test_rundown_cleanse():
    assert False

@pytest.mark.skip
@pytest.mark.service
def test_rundown_arrange():
    assert False


@pytest.mark.skip
@pytest.mark.service
def test_rundown_compress():
    assert False


# Parser tests.
from cro.rundown.sdk import RundownParser

import io

@pytest.fixture
def rundown():
    return io.StringIO("""\
        <


    """)


@pytest.mark.skip
@pytest.mark.service
def test_rundown_parse():
    assert False
