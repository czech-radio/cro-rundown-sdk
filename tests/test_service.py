# -*- coding: utf-8  -*-


import pytest


@pytest.mark.skip
@pytest.mark.service
def test_rundown_cleanse():
    assert False

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 4320dcd (Update date, time, duration parsing)
=======

>>>>>>> fac1de7 (Use black)
@pytest.mark.skip
@pytest.mark.service
def test_rundown_arrange():
    assert False


@pytest.mark.skip
@pytest.mark.service
def test_rundown_compress():
    assert False


<<<<<<< HEAD
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
=======
import io

>>>>>>> fac1de7 (Use black)
# Parser tests.
from cro.rundown.sdk import RundownParser


@pytest.fixture
def rundown():
    return io.StringIO(
        """\
        <


<<<<<<< HEAD
    """)
>>>>>>> 4320dcd (Update date, time, duration parsing)
=======
    """
    )
>>>>>>> fac1de7 (Use black)


@pytest.mark.skip
@pytest.mark.service
def test_rundown_parse():
    assert False
