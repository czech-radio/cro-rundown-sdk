# -*- coding: utf-8 -*-

import pytest

from cro.rundown.sdk._domain import Respondent


def test_respondent_model():

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
