# -*- coding: utf-8 -*-

import pytest

from cro.rundown.sdk._domain import Respondent, Name


@pytest.mark.domain
def test_respondent_model():

    respondent = Respondent(
        id="UUID",
        name=Name("David", "Landa"),
        affiliation="BEZPP",
        labels=["programmer"],
    )

    assert respondent.name.given == "David"
    assert respondent.name.family == "Landa"
    assert respondent.affiliation == "BEZPP"
    assert respondent.labels == ["programmer"]
