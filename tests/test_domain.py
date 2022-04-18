import pytest

from cro.broadcast.extracting.domain.respondent import Respondent


def test_model():

    respondent = Respondent(
        openmedia_id="UUID",
        affiliation="BEZPP",
        given_name="David",
        family_name="Landa",
        labels=["programmer"],
    )

    assert respondent.given_name == "David"
    assert respondent.family_name == "Landa"
    assert respondent.labels == ["programmer"]


def test_parsing():
    ...
