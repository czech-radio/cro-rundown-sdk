# -*- coding: utf-8 -*-

"""
The module with command line program.
"""


import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

from cro.rundown.sdk import RundownParser, table_columns
from cro.rundown.sdk.helpers import flatten


STATION_NAMES = {
    "nationwide": ("Plus", "Radiožurnál"),
    "regional": ("Olomouc", "Pardubice"),
}  # not complete


def main():
    """
    Extract the broadcast data from OpenMedia Rundown XML files.
    """
    load_dotenv()  # Take environment variables from `.env`.

    parser = argparse.ArgumentParser(description="The `cro.rundown.extract` program.")

    parser.add_argument("-i", "--input", required=True, help="The import directory.")
    parser.add_argument("-o", "--output", required=True, help="The export directory.")
    parser.add_argument(
        "-s",
        "--station",
        required=False,
        help="The station type: nationwide | regional | all",
    )
    parser.add_argument("--verbose", action="store_true")

    options = parser.parse_args()

    # ################################################################### #
    # [1] Load XML files in the given path.                               #
    # ################################################################### #
    import_path = Path(options.input)
    export_path = Path(options.output)

    if not import_path.is_dir():
        logger.error("The given import path must be a directory.")
        sys.exit(1)

    if not export_path.is_dir():
        logger.error("The given export path must be a directory.")
        sys.exit(1)

    if options.verbose:
        logger.info(f"RUNDOWN IMPORT PATH: {import_path}")
        logger.info(f"RUNDOWN EXPORT PATH: {export_path}")

    # TODO
    # if options.station is not None:
    #     match options.station:
    #         case "nationwide":
    #             STATIONS = STATION_NAMES["nationwide"]
    #         case "regional":
    #             STATIONS = STATION_NAMES["regional"]
    #         case _:
    #             print("Station type not recognized, use 'nationwide' or 'regional'.")
    #             sys.exit(1)
    # else:
    #     STATIONS = STATION_NAMES["nationwide"] + STATION_NAMES["regional"]

    parser = RundownParser()

    result: dict[str, list] = {}

    paths = (
        p
        for p in Path(import_path).glob("**/*.xml")
        if p.is_file() and any(s in p.stem for s in STATION_NAMES)  # [HARD CODED]
        # Use `any` vs `not any` for nationwide vs regional stations.
    )

    # ################################################################### #
    # [2] Parse XML files.                                                #
    # ################################################################### #
    errors = []
    for path in tqdm(paths):
        try:
            result[path.stem] = list(parser(ET.parse(path)))
        except Exception as ex:
            errors.append((path.stem, ex))

    # ################################################################### #
    # [3] Write CSV/XLSX files.                                           #
    # ################################################################### #
    df = pd.DataFrame([x for x in flatten(result.values()) if len(x) > 0])
    df = df[table_columns]

    print("---\n")
    print(df.size)
    print(date_min := df["date"].min())
    print(date_max := df["date"].max())
    print("\n---")

    output_file_name = f"RUNDOWN_{date_min}_{date_max}.xlsx"
    output_file_path = export_path / output_file_name

    with pd.ExcelWriter(output_file_path) as writer:
        df.to_excel(
            writer,
            sheet_name=f"RUNDOWN_{date_min}_{date_max}",
            index=False,
            header=True,
        )
    # TODO
    # Save the file at least to the root folder.
    # except IOError as ex:
    #   logger.warning(f"The file was writen to {path}.")

    if len(errors) > 0:
        logger.error("FINISHED with FAILURE")
        for path, error in errors:
            print(path, error)
        sys.exit(1)

    logger.info("FINISHED with SUCCESS")
