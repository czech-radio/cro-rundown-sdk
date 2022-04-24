# -*- coding: utf-8 -*-


"""
A domain model values, entities and services.
"""


import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from xml.etree.ElementTree import ElementTree

__all__ = tuple(["Rundown", "Respondent", "Station"])


# >>> internal


@dataclass(frozen=True)
class NonEmptyString:

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("A value must be non empty string.")


@dataclass(frozen=True)
class Name(NonEmptyString):
    ...


@dataclass(frozen=True)
class GivenName:
    value: str


@dataclass(frozen=True)
class FamilyName:
    value: str


@dataclass(frozen=True)
class FullName:
    given: GivenName
    family: FamilyName


@dataclass(frozen=True, eq=True)
class Label:
    name: str


class Respondent:
    """
    A respondent extracted form the rundown file.
    """

    def __init__(
        self,
        openmedia_id: str,
        given_name: str,
        family_name: str,
        labels: List[str],
        affiliation: str,
    ):
        self._full_name = FullName(GivenName(given_name), FamilyName(family_name))
        self._labels: List[str] = labels
        self._openmedia_id = openmedia_id
        self._affiliation = affiliation
        # gender

    @property
    def full_name(self) -> FullName:
        return self._full_name

    @property
    def given_name(self) -> str:
        return self.full_name.given.value

    @property
    def family_name(self) -> str:
        return self.full_name.family.value

    @property
    def labels(self) -> List[str]:
        return self._labels

    @property
    def political_affiliation(self):
        return self._affiliation

    def __str__(self) -> str:
        return f"Respondent{self.full_name}, {self.labels}"

    def __eq__(self, other) -> bool:
        return (self.full_name, self.labels, self.political_affiliation) == (
            other.full_name,
            other.profession,
            other.political_affiliation,
        )

    def __hash__(self) -> int:
        return hash((self.full_name, self.labels, self.political_affiliation))


# <<< internal


class StationType(Enum):
    REGIONAL = "regional"
    NATIONWIDE = "nationwide"
    # to string
    # from string


@dataclass(frozen=True)
class Station:
    id: int
    name: str
    type: StationType


@dataclass(frozen=True)
class Record:
    since: dt.time
    till: dt.time
    respondents: tuple[Respondent]


class Rundown:
    """
    The rundown domain model.
    """

    def __init__(
        self,
        date,
        station: Station,
        cleaned_content: ElementTree,
        cleaned_name: str,
        original_name: Optional[str] = None,
        original_content: Optional[ElementTree] = None,
    ):
        self.date = date
        self.station = station
        self.cleaned_name = cleaned_name
        self.original_name = original_name
        self.cleaned_content = cleaned_content
        self.original_content = original_content

    @property
    def records(self) -> tuple[Record]:
        return tuple([])

    # == equality
    # >  ordering
    # hash
