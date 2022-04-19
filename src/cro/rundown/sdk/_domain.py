# -*- coding: utf-8 -*-

"""
WORK IN PROGRESS
"""

from typing import List, NamedTuple
from xml.etree.ElementTree import fromstring

__all__ = tuple(["Rundown", "Respondent"])


from dataclasses import InitVar, dataclass, field
from typing import NamedTuple

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

from enum import Enum


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


class Rundown:
    def __init__(self, date, station: Station):
        self.date = date
        self.station = station

    @property
    def records(self) -> tuple["Record"]:
        return tuple([])
