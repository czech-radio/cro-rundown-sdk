# -*- coding: utf-8 -*-


import argparse
import datetime
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple

import pandas as pd
from loguru import logger
from tqdm import tqdm

__all__ = tuple(["RundownParser", "ParseRundown"])


def parse_rundown(xml):
    tree = ET.parse(xml)

    # > Radio Rundown OM_OBJECT: only one node.
    rr = tree.find('.//*[@TemplateName="Radio Rundown"]')

    # > Hourly Rundown(s) OM_RECORD.OM_OBJECT(s)
    for hr in rr.findall('.//*[@TemplateName="Hourly Rundown"]'):

        # > Sub Rundown(s) OM_OBJECT(s)
        for sr in hr.findall('.//*[@TemplateName="Sub Rundown"]'):

            for od in sr.findall(".//OM_RECORD"):

                for ob in od.findall(".//OM_OBJECT"):
                    header = ob.find(".//OM_HEADER")
                    # print(f'<{hr.tag} {hr.attrib["ObjectID"]} {hr.attrib["TemplateName"]}><{sr.tag} {sr.attrib["ObjectID"]} {sr.attrib["TemplateName"]}><{ob.tag} {ob.attrib["TemplateName"]}')
                    match ob.attrib["TemplateName"]:
                        case "Radio Story":
                            # print(f'{"Story"}: {ob.attrib["ObjectID"]}')
                            ...
                        case "Audioclip":
                            ...
                            # print(f'{"Sudio"}: {ob.attrib["ObjectID"]}')

    return tree


class RundownParser:
    """
    Parse rundown XML files to get a brodcast data for further analysis.

    >>> parser = RundownParser(path=Path("."))
    >>> for file, data in parser
            ... # process data
    """

    def __init__(self, path: Path) -> None:
        if not path.is_dir():
            raise ValueError("Path must be a directory.")
        self._path: Path = path
        self._errors: List = []

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        self._path = path

    @property
    def errors(self) -> List:
        return self._errors.copy()

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __iter__(self) -> Generator[Tuple[object, dict], None, None]:
        """
        Parse the  rundown XML files one by one.
        TODO: Make the parsing concurent/parallel.

        :returns: The generator of parsed file objects.
        """
        # Load all rundown XML files in the given path (recursively)
        for path in Path(self.path).glob("**/*.xml"):
            if not path.is_file():
                continue
            try:
                root = ET.parse(path).getroot()

                if (
                    rundowns := root.find("./OM_OBJECT[@TemplateName='Radio Rundown']")
                ) is None:
                    continue

                top_level_nodes = [x for x in rundowns]
                header, records = top_level_nodes[0], top_level_nodes[1:]
                date = self._extract_date(header)
                station_id = self._extract_station_id(header)

                for record in records:
                    time = self._extract_time(record)
                    duration = self._extract_duration(record)

                    if (
                        subobject := record.find(
                            "./OM_OBJECT[@TemplateName='Hourly Rundown']"
                        )
                    ) is None:
                        # todo: Log this!
                        continue

                    for subrecord in subobject.findall("./OM_RECORD"):
                        title = self._extract_title(subrecord)

                        for subsubrecord in subrecord.findall("./OM_OBJECT/OM_RECORD"):
                            topic = self._extract_topic(subsubrecord)
                            subtitle = self._extract_subtitle(subsubrecord)
                            format = self._extract_format(subsubrecord)
                            author = self._extract_author(subsubrecord)
                            editorial = self._extract_editorial(subsubrecord)
                            approved = self._extract_approved(subsubrecord)
                            incode = self._extract_incode(subsubrecord)
                            itemcode = self._extract_itemcode(subsubrecord)

                            for om_object in subsubrecord.findall(
                                ".//OM_OBJECT[@TemplateName='Contact Item']"
                            ):
                                openmedia_id = self._extract_unique_id(om_object)
                                given_name = self._extract_given_name(om_object)
                                family_name = self._extract_family_name(om_object)
                                labels = self._extract_labels(om_object)
                                gender = self._extract_gender(om_object)
                                affiliation = self._extract_affiliation(om_object)

                                yield path, OrderedDict(
                                    [
                                        ("date", date),
                                        ("time", time),
                                        ("duration", duration),
                                        ("station_id", station_id),
                                        ("title", title),
                                        ("subtitle", subtitle),
                                        ("format", format),
                                        ("author", author),
                                        ("approved", approved),
                                        ("editorial", editorial),
                                        ("incode", incode),
                                        ("itemcode", itemcode),
                                        ("topic", topic),
                                        ("openmedia_id", openmedia_id),
                                        ("given_name", given_name),
                                        ("family_name", family_name),
                                        ("labels", labels),
                                        ("gender", gender),
                                        ("affiliation", affiliation),
                                    ]
                                )
            except Exception as ex:
                self._errors.append((str(path), str(ex)))
                yield path, None
                continue

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

    def _extract_title(self, om_object: ET.Element) -> Optional[str]:
        """
        Extract the title in the objects header section.
        """
        return self._extract_text(
            element=om_object, xpath="./OM_FIELD[@FieldID='8']/OM_STRING"
        )

    def _extract_subtitle(self, om_object: ET.Element) -> Optional[str]:
        """
        Extract the title in the objects header section.
        """
        return self._extract_text(
            element=om_object, xpath="./OM_FIELD[@FieldID='8']/OM_STRING"
        )

    def _extract_topic(self, om_record: ET.Element) -> Optional[str]:
        """
        Extract the title.
        """
        return self._extract_text(
            element=om_record, xpath="./OM_FIELD[@FieldID='5016']/OM_STRING"
        )

    def _extract_duration(self, om_record: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=om_record, xpath="./OM_FIELD[@FieldID='1005']/OM_TIMESPAN"
        )

    def _extract_date(self, header) -> Optional[str]:
        """
        Extract the date.
        """
        text = self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='1000']/OM_DATETIME"
        )

        if text is None:
            return None
        else:
            text = text.split("T")[0]

        return str(datetime.datetime.strptime(text, "%Y%m%d").date())

    def _extract_time(self, om_record: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=om_record, xpath="./OM_FIELD[@FieldID='8']/OM_STRING"
        )

    def _extract_station_id(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='5081']/OM_INT32"
        )

    def _extract_author(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='6']/OM_STRING"
        )

    def _extract_approved(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='5070']/OM_STRING"
        )

    def _extract_incode(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='5072']/OM_STRING"
        )

    def _extract_itemcode(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='5082']/OM_STRING"
        )

    def _extract_editorial(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='12']/OM_STRING"
        )

    def _extract_format(self, header: ET.Element) -> Optional[str]:
        return self._extract_text(
            element=header, xpath="./OM_FIELD[@FieldID='321']/OM_INT32"
        )

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


# ########################################################################### #
# ########################################################################### #
# ########################################################################### #
#          PARSE THE GIVEN XML RUNDOWN FILES AND WRITE DATA TO CSV.
# ########################################################################### #"
# ########################################################################### #"
# ########################################################################### #"

STATON_CODE_NAME: Dict[int, str] = {
    3: "UN",
    5: "CR",
    11: "RZ",
    13: "PS",
    15: "DV",
    17: "VL",
    19: "WA",
    21: "RJ",
    23: "ZV",
    31: "RD",
    33: "SC",
    35: "PN",
    37: "KV",
    39: "SE",
    41: "LB",
    43: "HK",
    45: "PC",
    47: "CB",
    49: "VY",
    51: "BO",
    53: "OL",
    55: "OV",
    57: "ZL",
    73: "RG",
    75: "RE",
}


def main():
    """
    Reads and parse openmedia XML files and acquires the broadcast data
    for future data manual cleanning.
    """
    import os
    import sys

    from dotenv import load_dotenv

    load_dotenv()  # Take environment variables from `.env`.

    try:
        parser = argparse.ArgumentParser(
            description="The respondent mathching (pairing)."
        )
        parser.add_argument(
            "-w", "--week", required=True, help="A week number in form `MM`."
        )
        # TODO: month | period
        parser.add_argument(
            "-y", "--year", required=True, help="A year number in form `YYYY`."
        )
        options = parser.parse_args()

        year: int = options.year
        week: int = (
            f"0{options.week}" if int(options.week) < 9 else options.week
        )  # Prepend with zero.

        RUNDOWN_EXPORT_PATH = os.getenv("RUNDOWN_EXPORT_PATH")

        print(RUNDOWN_EXPORT_PATH)

        import_path = Path(RUNDOWN_EXPORT_PATH) / f"{year}" / f"W{week}"
        export_path = Path(f"G:/My Drive/Rozhlas/Analytics/Source/{year} Zpravodajství")

        # ========================================================================
        # Task 1: Parse XML files.
        # ========================================================================
        # if int(week) < 9: week = f"0{week}" # Prepend with zero when.

        # Note thath the path depends on your locale e.g. G:\My Drive vs G:\Můj disk
        output_file_name = f"DATA_{year}W{week}.xlsx"
        output_file_path = export_path / output_file_name

        parser = RundownParser(path=import_path)

        result: Dict[str, list] = {}

        with tqdm() as pbar:
            for file, data in parser:
                if data is None:
                    pbar.write(f"PROCESSING FILE FAILURE: {file.stem}")
                else:
                    result[data.values()] = data
                    pbar.write(f"PROCESSING FILE SUCCESS: {file.stem}")
                pbar.update(1)

        if parser.has_errors():
            logger.error(parser.errors)

        # ========================================================================
        # Task 2. Write CSV and XLSX files.
        # ========================================================================
        # TODO Report and remove empty lists from result data.
        df = pd.DataFrame([x for x in result.values() if len(x) > 0])

        df.to_excel(output_file_path, sheet_name=f"SOURCE_W{week}", index_label="index")

        logger.info("FINISHED with SUCCESS")

    except IOError as ex:
        # Save the file to the root folder when Google Drive fails.
        # This is better then start from beginning :/
        try:
            # df.to_excel(
            #     Path("./") / output_file_name,
            #     sheet_name=f"SOURCE_W{week}",
            #     index_label="index",
            # )
            logger.warning(f"The file was writen to the root folder: {ex}.")
        except Exception as ex:
            raise ex

    except Exception as ex:
        logger.error(ex)
        logger.info("FINISHED with FAILURE")
    finally:
        logger.info("=====================")
