# -*- coding: utf-8 -*-

"""
The rundown file data extraction.
"""

from __future__ import annotations

import sys
import datetime
import datetime as dt
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple

from loguru import logger

__all__ = tuple(["RundownParser"])


class RundownParser:
    """
    Parse rundown XML files to get a brodcast data for further analysis.

    >>> parser = RundownParser(path=Path("."))
    >>> for file, data in parser
            ... # process data
    """

    def __init__(self) -> None:
        self._files = []
        self._errors: List = []

    @property
    def files(self) -> tuple[Path]:
        return tuple(self._files)

    @property
    def errors(self) -> List:
        return tuple(self._errors)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __call__(self, rundowns: dict[str, ET.ElementTree]) -> RundownParser:
        self._files = rundowns
        return self

    def __iter__(self) -> Generator[Tuple[object, dict], None, None]:
        """
        Parse the  rundown XML files one by one.
        TODO: Make the parsing concurrent/parallel.

        :returns: The generator of parsed file objects.
        """

        for path, rundown in self._files.items():

            PROCESED_FILES: dict[str, str] = {}

            try:
                root = rundown.getroot()

                # [1] Radion Rundown
                if (
                    radio_rundown := root.find(
                        "./OM_OBJECT[@TemplateName='Radio Rundown']"
                    )
                ) is None:
                    # Skip the file but report to statistics.
                    PROCESED_FILES[path] = "NOT PROCESSED"
                    continue

                date = self._extract_date(radio_rundown[0])
                hours_station_date: str = self._extract_station_date_hours(
                    radio_rundown[0]
                )

                # [2]
                for record in (hourly_rundown_records := radio_rundown[1:]):

                    station_id = self._extract_station_id(record)
                    title = self._extract_title(record)

                    if (
                        hourly_rundown_object := record.find(
                            "./OM_OBJECT[@TemplateName='Hourly Rundown']"
                        )
                    ) is None:
                        # todo: Log this!
                        print("NEOBSAHUJE HOURLY RUNDOWN")
                        # continue
                        sys.exit()

                    oid = hourly_rundown_object.attrib["ObjectID"]
                    otn = hourly_rundown_object.attrib["TemplateName"]
                    hour_block = self._extract_station_hour_block(hourly_rundown_object)

                    for record in hourly_rundown_object.findall("./OM_RECORD"):

                        author = self._extract_author(record)
                        creator = self._extract_creator(record)
                        editorial = self._extract_editorial(record)
                        approved_station = self._extract_approved_station(
                            record
                        )  # schválil za redakci
                        approved_editorial = self._extract_approved_editorial(
                            record
                        )  # schválil za stanici
                        title = self._extract_title(record)
                        topic = self._extract_topic(record)
                        target = self._extract_text(
                            record, "./OM_FIELD[@FieldID='5079']/OM_STRING"
                        )  # cíl výroby


                        for obj in record.findall(
                            './/OM_OBJECT[@TemplateName="Radio Story"]'
                        ):
                            header = obj.find("./OM_HEADER")

                            duration_maybe = self._extract_duration(header)
                            duration = duration_maybe if duration_maybe is not None else "0"

                            format = self._extract_format(header)
                            incode = self._extract_incode(header)
                            itemcode = self._extract_itemcode(header)
                            subtitle = self._extract_title(header)

                            time = self._extract_time(header)

                            # >>> Parse respondet data.
                            # for om_object in record.findall(
                            #     ".//OM_OBJECT[@TemplateName='Contact Item']"
                            # ):
                            #     openmedia_id = self._extract_unique_id(om_object)
                            #     given_name = self._extract_given_name(om_object)
                            #     family_name = self._extract_family_name(om_object)
                            #     labels = self._extract_labels(om_object)
                            #     gender = self._extract_gender(om_object)
                            #     affiliation = self._extract_affiliation(om_object)
                            # <<<
                            data = OrderedDict(
                                [
                                    # ANOVA DATA
                                    # ("oid", oid),
                                    # ("tn", otn),
                                    # BROADCAST DATA
                                    (
                                        "station",
                                        station_id,
                                    ),  # TODO: Add alo station name.
                                    ("date", date),
                                    ("block", hour_block),
                                    # TODO: Add `since` (datum začátku).
                                    ("time",  dt.datetime.strptime(time, "%Y%m%dT%H%M%S,%f").time()),
                                    (
                                        "duration",
                                        str(round(float(duration) / 1000 / 600, 1)),
                                    ),  # ms to min
                                    ("target", target),
                                    ("itemcode", itemcode),
                                    ("incode", incode),
                                    ("title", title),
                                    ("subtitle", subtitle),
                                    ("format", format),
                                    ("author", author),
                                    ("creator", creator),
                                    ("editorial", editorial),
                                    ("approved_station", approved_station),
                                    ("approved_editorial", approved_editorial),
                                    ("topic", topic),
                                    # RESPONDENT DATA
                                    # ("openmedia_id", openmedia_id),
                                    # ("given_name", given_name),
                                    # ("family_name", family_name),
                                    # ("labels", labels),
                                    # ("gender", gender),
                                    # ("affiliation", affiliation),
                                ]
                            )
                            data_cleaned = {
                                k: str(v).strip()
                                for k, v in data.items()
                                if v is not None
                            }
                            # print(  "|".join([f"{v}" for k, v in data_cleaned.items()]) ) # DEBUG
                            yield path, data_cleaned

            except Exception as ex:
                logger.error(ex)
                self._errors.append((str(path), str(ex)))
                raise ex

    def _extract_text(self, element: ET.Element, xpath: str) -> Optional[str]:
        """
        Extract the text from the given XML node e.g
        from `<node>text</node>` extract `text`.
        """
        node = element.find(xpath)
        return None if node is None else node.text

    def _extract_text_from_header_field(
        self,
        element: ET.Element,
        field_id: int,
        element_name: str = "OM_STRING",
    ) -> Optional[str]:
        return self._extract_text(
            element=element,
            xpath=f"./OM_HEADER/OM_FIELD[@FieldID='{field_id}']/{element_name}",
        )

    # BROADCAST DATA #

    def _extract_title(self, element: ET.Element) -> Optional[str]:
        """Extract the field with title content."""
        return self._extract_text(element, "./OM_FIELD[@FieldID='8']/OM_STRING")

    def _extract_topic(self, element: ET.Element) -> Optional[str]:
        """Extract the field with topic content."""
        return self._extract_text(element, "./OM_FIELD[@FieldID='5016']/OM_STRING")

    def _extract_station_date_hours(self, element):
        return self._extract_text(element, "./OM_FIELD[@FieldID='8']/OM_STRING")

    def _extract_station_hour_block(self, hourly_rundown_object):
        return self._extract_text(
            element=hourly_rundown_object,
            xpath="./OM_HEADER/OM_FIELD[@FieldID='8']/OM_STRING",
        )

    def _extract_date(self, element) -> Optional[str]:
        """
        Extract the date.
        """
        text = self._extract_text(element, "./OM_FIELD[@FieldID='1000']/OM_DATETIME")
        return (text if text is None else str(datetime.datetime.strptime(text.split("T")[0], "%Y%m%d").date()))

    def _extract_time(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='1003']/OM_DATETIME")

    def _extract_duration(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='1026']/OM_TIMESPAN")

    def _extract_station_id(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5081']/OM_INT32")

    def _extract_author(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element,"./OM_FIELD[@FieldID='6']/OM_STRING")

    def _extract_creator(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5']/OM_STRING")

    def _extract_approved_station(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5071']/OM_STRING")

    def _extract_approved_editorial(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5070']/OM_STRING")

    def _extract_incode(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5072']/OM_STRING")

    def _extract_itemcode(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5082']/OM_STRING")

    def _extract_editorial(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='12']/OM_STRING")

    def _extract_format(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='321']/OM_INT32")

    # RESPONDENT DATA #

    def _extract_unique_id(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element=element, field_id=5087)

    def _extract_given_name(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element=element, field_id=421)

    def _extract_family_name(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element=element, field_id=422)

    def _extract_labels(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element=element, field_id=424)

    def _extract_gender(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(
            element=element, field_id=5088, element_name="OM_INT32"
        )

    def _extract_affiliation(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element=element, field_id=5015)
