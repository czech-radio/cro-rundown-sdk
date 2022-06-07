# -*- coding: utf-8 -*-

"""
The rundown file data extraction.
"""

from __future__ import annotations

import datetime
import datetime as dt
import math
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path
from typing import Generator, List, Optional

from loguru import logger

__all__ = tuple(["RundownParser", "format_code_vs_names", "table_columns"])


format_code_vs_name = {
    "2901": "čtená",
    "2903": "zvuk",
    "2905": "živý vstup",
    "2907": "rsm",
    "2909": "rozhovor",
    "2911": "montáž",
    "2913": "reportáž",
    "2915": "názory",
    "2917": "událost",
    "2919": "pořad",
    "2921": "předěl",
    "2923": "promo",
    "701": "respondent",
    "703": "kontakt",
    "2701": "zprávy",
    "2703": "commercial",
    "2705": "proud",
    "2707": "plán - zprávy",
}


# Table columns for export.
table_columns = [
    # "oid",
    # "rr_rid",
    # "hr_rid",
    # "category1",
    # "category2",
    "category",  # aka category 3
    "station",
    "date",
    "block",
    "since",
    "till",
    "duration",
    "format",
    "target",
    "itemcode",
    "incode",
    "topic",
    "creator",
    "author",
    "editorial",
    "approved_station",
    "approved_editorial",
    "title1",
    "title2",
    "title3",
]


def postprocess_result(dct: dict) -> pd.DataFrame:
    """Post process the parsed values."""
    # Post process the pandas dataframe: normalize = lowercase, strip, replace...


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
    def errors(self) -> List:
        return tuple(self._errors)

    def __call__(self, rundown: ET.ElementTree) -> Generator[OrderedDict, None, None]:
        """
        Parse the  rundown XML files one by one.
        TODO: Make the parsing concurrent/parallel.

        :returns: The generator of parsed file objects.
        """
        try:
            root = rundown.getroot()

            # [1] RADIO RUNDOWN OBJECT
            if (
                radio_rundown := root.find("./OM_OBJECT[@TemplateName='Radio Rundown']")
            ) is None:
                return "RADIO RUNDOWN NOT FOUND"

            date = self._extract_date(radio_rundown[0])  # [0] => first node = header
            # hours_station_date: str = self._extract_station_date_hours(radio_rundown[0])

            # [2] RADIO RUNDOWN (HOURLY BLOCK) RECORDS
            for rr_record in radio_rundown.findall("./OM_RECORD"):

                rr_record_id = rr_record.attrib["RecordID"]

                # [3] HOURLY RUNDOWN OBJECT (one for each hourly block record)
                if (
                    hourly_rundown_object := rr_record.find(
                        "./OM_OBJECT[@TemplateName='Hourly Rundown']"
                    )
                ) is None:
                    logger.error("NEOBSAHUJE HOURLY RUNDOWN")
                    continue  # or sys.exit(1) ?

                hour_block = self._extract_station_hour_block(hourly_rundown_object)

                category1 = hourly_rundown_object.attrib["TemplateName"]

                # [4] HOURLY RUNDOWN RECORDS
                for hr_record in hourly_rundown_object.findall("./OM_RECORD"):
                    title1 = str(self._extract_title(hr_record)).replace("=", "#")
                    hr_record_id = hr_record.attrib["RecordID"]

                    duration = self._extract_duration(hr_record)
                    if duration is not None:
                        duration = math.ceil(int(duration) / 1000 / 60)  # minutes

                    # [5] RADIO STORY
                    for obj in hr_record.findall(
                        './/OM_OBJECT[@TemplateName="Radio Story"]'
                    ):

                        header = obj.find("./OM_HEADER")

                        oid = obj.attrib["ObjectID"]
                        otn = obj.attrib["TemplateName"]

                        format_code = self._extract_format(header)
                        format_name = format_code_vs_name.get(format_code, "")

                        incode = self._extract_incode(header)
                        itemcode = self._extract_itemcode(header)
                        title2 = str(self._extract_title(header)).replace("=", "#")
                        category2 = self._extract_text(
                            header, "./OM_FIELD[@FieldID='5001']/OM_STRING"
                        )

                        target = self._extract_target(header)
                        if target is not None:
                            target = target.lower().strip()

                        station_id = self._extract_station_id(header)
                        author = self._extract_author(header)
                        creator = self._extract_creator(header)

                        editorial = self._extract_editorial(header)
                        if editorial is not None:
                            editorial = editorial.replace("-", "###").strip()

                        approved_station = self._extract_approved_station(header)
                        approved_editorial = self._extract_approved_editorial(header)
                        topic = self._extract_topic(header)
                        since = self._extract_since(header)
                        till = self._extract_till(header)
                        time = self._extract_time(header)

                        if time is not None:
                            time = dt.datetime.strptime(time, "%Y%m%dT%H%M%S,%f").time()

                        if since is not None:
                            since = dt.datetime.strptime(
                                since, "%Y%m%dT%H%M%S,%f"
                            ).time()

                        if till is not None:
                            till = dt.datetime.strptime(till, "%Y%m%dT%H%M%S,%f").time()

                        result_part1 = OrderedDict(
                            [
                                # SYSTEM
                                # ("oid", oid),
                                # ("tn", otn),
                                # ("rr_rid", rr_record_id),
                                # ("hr_rid", hr_record_id),
                                ("category1", category1),
                                ("category2", category2),
                                # BROADCAST
                                ("station", station_id),
                                ("date", date),
                                ("block", hour_block),
                                ("since", since),
                                ("till", till),
                                ("duration", duration),
                                ("target", target),
                                ("itemcode", itemcode),
                                ("incode", incode),
                                ("title1", title1),
                                ("title2", title2),
                                ("format", format_name),
                                ("author", author),
                                ("creator", creator),
                                ("editorial", editorial),
                                ("approved_station", approved_station),
                                ("approved_editorial", approved_editorial),
                                ("topic", topic),
                            ]
                        )

                        result_parts2 = []
                        # [6] RECORDS in stories e.g. contact, audio etc. (may not be present)
                        for rs_record in (rs_records := obj.findall("./OM_RECORD")):
                            logger.debug(
                                f"Radio Rundown Record ID = {rr_record_id}, Hourly Rundown Record ID = {hr_record_id}, Radio Story Record ID {rs_record.attrib['RecordID']}"
                            )
                            title3 = (
                                str(self._extract_title(rs_record))
                                .replace("=", "#")
                                .strip()
                            )

                            category3 = self._extract_text(
                                rs_record, "./OM_FIELD[@FieldID='5001']/OM_STRING"
                            )

                            if category3 is not None:
                                category3 = (
                                    category3.replace("Item", "")
                                    .replace("Bin", "")
                                    .strip()
                                    .lower()
                                )

                            # if ".//OM_OBJECT[@TemplateName='Contact Item']"
                            #   openmedia_id = self._extract_unique_id(om_object)
                            #   given_name = self._extract_given_name(om_object)
                            #   family_name = self._extract_family_name(om_object)
                            #   labels = self._extract_labels(om_object)
                            #   gender = self._extract_gender(om_object)
                            #   affiliation = self._extract_affiliation(om_object)
                            # <<<
                            result_part2 = OrderedDict(
                                [
                                    # SYSTEM
                                    ("category", category3),
                                    # BROADCAST
                                    ("itemcode", itemcode),
                                    ("title3", title3),
                                    # RESPONDENT
                                    # ("openmedia_id", openmedia_id),
                                    # ("given_name", given_name),
                                    # ("family_name", family_name),
                                    # ("labels", labels),
                                    # ("gender", gender),
                                    # ("affiliation", affiliation),
                                ]
                            )
                            result_parts2.append(result_part2)

                        results = (
                            [result_part1 | rp2 for rp2 in result_parts2]
                            if len(result_parts2)
                            else [result_part1 | {"category3": None, "title3": None}]
                        )

                        for result in results:
                            yield {
                                k: str(v).strip()
                                for k, v in result.items()
                                if v is not None
                            }

        except Exception as ex:
            logger.error(ex)
            self._errors.append((str(), str(ex)))
            # raise ex

    def _extract_text(self, element: ET.Element, xpath: str) -> Optional[str]:
        """
        Extract the text from the given XML node e.g
        from `<node>text</node>` extract `text`.
        """
        result = None

        if (node := element.find(xpath)) is not None:
            if (text := node.text) is not None:
                result = text.strip()

        return result

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

    # BROADCAST#

    def _extract_title(self, element: ET.Element) -> Optional[str]:
        """Extract the field with title content."""
        return self._extract_text(element, "./OM_FIELD[@FieldID='8']/OM_STRING")

    def _extract_topic(self, element: ET.Element) -> Optional[str]:
        """Extract the field with topic content."""
        return self._extract_text(element, "./OM_FIELD[@FieldID='5016']/OM_STRING")

    def _extract_station_date_hours(self, element):
        return self._extract_text(element, "./OM_FIELD[@FieldID='8']/OM_STRING")

    def _extract_station_hour_block(self, hr_object):
        return self._extract_text(
            element=hr_object, xpath="./OM_HEADER/OM_FIELD[@FieldID='8']/OM_STRING"
        )

    def _extract_date(self, element) -> Optional[str]:
        text = self._extract_text(element, "./OM_FIELD[@FieldID='1000']/OM_DATETIME")
        return (
            text
            if text is None
            else str(datetime.datetime.strptime(text.split("T")[0], "%Y%m%d").date())
        )

    def _extract_since(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='1000']/OM_DATETIME")

    def _extract_till(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='1001']/OM_DATETIME")

    def _extract_time(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='1003']/OM_DATETIME")

    def _extract_target(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5079']/OM_STRING")

    def _extract_duration(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='1026']/OM_TIMESPAN")

    def _extract_station_id(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='5081']/OM_INT32")

    def _extract_author(self, element: ET.Element) -> Optional[str]:
        return self._extract_text(element, "./OM_FIELD[@FieldID='6']/OM_STRING")

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

    # RESPONDENT#

    def _extract_unique_id(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element, 5087)

    def _extract_given_name(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element, 421)

    def _extract_family_name(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element, 422)

    def _extract_labels(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element, 424)

    def _extract_gender(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element, 5088, "OM_INT32")

    def _extract_affiliation(self, element: ET.Element) -> Optional[str]:
        return self._extract_text_from_header_field(element, 5015)

    # function
    # expertise
    # email
    # phone
