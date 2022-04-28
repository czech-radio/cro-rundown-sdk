# -*- coding: utf-8  -*-


import pytest



@pytest.mark.skip
@pytest.mark.service
def test_rundown_cleanse():
    assert False

<<<<<<< HEAD

=======
>>>>>>> 4320dcd (Update date, time, duration parsing)
@pytest.mark.skip
@pytest.mark.service
def test_rundown_arrange():
    assert False


@pytest.mark.skip
@pytest.mark.service
def test_rundown_compress():
    assert False


<<<<<<< HEAD
import io

# Parser tests.
from cro.rundown.sdk import RundownParser


@pytest.fixture
def rundown():
    return io.StringIO(
        """\
        <


    """
    )
=======
# Parser tests.
from cro.rundown.sdk import RundownParser

import io

@pytest.fixture
def rundown():
    return io.StringIO("""\
        <


    """)
>>>>>>> 4320dcd (Update date, time, duration parsing)


@pytest.mark.skip
@pytest.mark.service
def test_rundown_parse():
    assert False
