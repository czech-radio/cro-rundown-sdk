# -*- coding: utf-8 -*-


"""
A domain model values, entities and services.
"""


import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from xml.etree.ElementTree import ElementTree

__all__ = tuple(["Rundown", "Respondent", "Station", "Name"])



@dataclass(frozen=True)
class Name:
    given: str
    family: str

    def __post_init__(self):
        if self.given is None or len(self.given) == 0:
            raise ValueError("The given name value must be non empty string.")
        if self.family is None or len(self.family) == 0:
            raise ValueError("The family name value must be non empty string.")


@dataclass(frozen=True)
class Respondent:
    """
    A respondent extracted form the rundown file.

    :param id: The idetifier stored in OpenMedia system.
    :param name: The person name.
    :param labels: The associated description labels e.g 'profession'.
    :param affiliation: The associated political affiliation e.g 'party name'.
    """
    id: str
    name: Name
    labels: List[str]
    affiliation: str
    gender: str = None


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
