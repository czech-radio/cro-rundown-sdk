# -*- coding: utf-8 -*-


import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

from cro.rundown.sdk import RundownParser


def main():
    """
    Extract the broadcast data from OpenMedia Rundown XML files.
    """

    load_dotenv()  # Take environment variables from `.env`.

    parser = argparse.ArgumentParser(description="The respondent mathching (pairing).")
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

    try:
        RUNDOWN_IMPORT_PATH = os.getenv("RUNDOWN_IMPORT_PATH_TEST_LOCAL")
        RUNDOWN_EXPORT_PATH = os.getenv("RUNDOWN_EXPORT_PATH_TEST_LOCAL")

        import_path = Path(f"{RUNDOWN_IMPORT_PATH}/{year}/W{week}")
        export_path = Path(f"{RUNDOWN_EXPORT_PATH}/{year}/W{week}")

        print(import_path)
        print(export_path)

        # ========================================================================
        # Task 1: Parse XML files.
        # ========================================================================
        # if int(week) < 9: week = f"0{week}" # Prepend with zero when.

        # Note thath the path depends on your locale e.g. G:\My Drive vs G:\Můj disk
        output_file_name = f"DATA_{year}W{week}.xlsx"
        output_file_path = export_path / output_file_name

        parser = RundownParser()

        result: Dict[str, list] = {}

        with tqdm() as pbar:
            for file, data in parser(directory=import_path):
                if data is None:
                    pbar.write(f"PROCESSING FILE FAILURE: {file.stem}")
                else:
                    result[data.values()] = data
                    # pbar.write(f"PROCESSING FILE SUCCESS: {file.stem}")
                pbar.update(1)

        if parser.has_errors():
            logger.error(parser.errors)

        # ========================================================================
        # Task 2. Write CSV and XLSX files.
        # ========================================================================
        # TODO Report and remove empty lists from result data.
        df = pd.DataFrame([x for x in result.values() if len(x) > 0])

        df.to_excel(output_file_path, sheet_name=f"SOURCE_W{week}", index=False)

        logger.info("FINISHED with SUCCESS")

    except IOError as ex:
        # Save the file to the root folder when Google Drive fails.
        # This is better then start from beginning :/
        try:
            df.to_excel(
                Path("./") / output_file_name,
                sheet_name=f"SOURCE_W{week}",
                index=False,
            )
            logger.warning(f"The file was writen to the root folder: {ex}.")
        except Exception as ex:
            raise ex

    except Exception as ex:
        logger.error(ex)
        logger.info("FINISHED with FAILURE")
    finally:
        logger.info("=====================")
