# -*- coding: utf-8 -*-

"""
The module with command line program.
"""


import argparse
import xml.etree.ElementTree as ET
import sys
from pathlib import Path
from time import time

import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

from cro.rundown.sdk import RundownParser


def flatten(t):
    return [item for sublist in t for item in sublist]


def main():
    """
    Extract the broadcast data from OpenMedia Rundown XML files.
    """

    load_dotenv()  # Take environment variables from `.env`.

    parser = argparse.ArgumentParser(description="The `cro.rundown.extract` program.")

    parser.add_argument("-i", "--input", required=True, help="The import directory.")

    parser.add_argument("-o", "--output", required=True, help="The export directory.")

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

    parser = RundownParser()
    result: dict[str, list] = {}
    paths = (
        p
        for p in Path(import_path).glob("**/*.xml")
        if p.is_file() and any(s in p.stem for s in ("Plus", "Radiožurnál")) # [HARD CODED]
    )

    # ################################################################### #
    # [2] Parse XML files.                                                #
    # ################################################################### #
    try:
        for path in tqdm(paths):
            result[path.stem] = list(parser(ET.parse(path)))

        # ################################################################### #
        # [3] Write CSV/XLSX files.                                           #
        # ################################################################### #

        df = pd.DataFrame([x for x in flatten(result.values()) if len(x) > 0])
        df = df[
            [
                "oid",
                "rr_rid",
                "hr_rid",
                # "category1",
                # "category2",
                "category3",
                "station",
                "date",
                "block",
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
        ]

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

        logger.info("FINISHED with SUCCESS")

    except IOError as ex:
        # Save the file at least to the root folder.
        with pd.ExcelWriter(path := Path(output_file_name)) as writer:
            df.to_excel(
                writer,
                sheet_name=f"SOURCE_{date_min}_{date_max}",
                index=False,
                header=True,
            )
            logger.warning(f"The file was writen to {path}.")

    except Exception as ex:
        logger.error("FINISHED with FAILURE")
        raise ex
