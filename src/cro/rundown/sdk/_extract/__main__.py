# -*- coding: utf-8 -*-


import argparse
import os
from pathlib import Path
import logging
from time import time
import xml.etree.ElementTree as ET


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

    parser = argparse.ArgumentParser(description="The `cro.rundown.extract` program.")

    parser.add_argument(
        "-w", "--week", required=True, help="A week number in form `MM`."
    )

    # TODO: month | period

    parser.add_argument(
        "-y", "--year", required=True, help="A year number in form `YYYY`."
    )

    parser.add_argument("--verbose", action="store_true")

    options = parser.parse_args()

    year: int = options.year
    week: int = (
        f"0{options.week}" if int(options.week) < 9 else options.week
    )

    try:

        # TODO: Check the paths, maybe set sensible defaults?
        import_path = Path(f"{os.getenv('RUNDOWN_IMPORT_PATH_TEST_LOCAL')}/{year}/W{week}")
        export_path = Path(f"{os.getenv('RUNDOWN_EXPORT_PATH_TEST_LOCAL')}/{year}/W{week}")

        if options.verbose:
            print(f"RUNDOWN IMPORT PATH: {import_path}")
            print(f"RUNDOWN EXPORT PATH: {export_path}")

        #
        # [1] Parse XML files.
        #

        # if int(week) < 9: week = f"0{week}" # Prepend with zero when.

        # Note thath the path depends on your locale e.g. G:\My Drive vs G:\Můj disk
        output_file_name = f"DATA_{year}W{week}.xlsx"
        output_file_path = export_path / output_file_name

        parser = RundownParser()

        result: dict[str, list] = {}

        # if not directory.is_dir():
        #     raise ValueError("The given path  must be a directory.")

        # Load all rundown XML files in the given path (recursively)
        rundowns = {
            path.stem: ET.parse(path) for path in Path(import_path).glob("**/*.xml") if path.is_file()
        }

        with tqdm() as pbar:
            start_time = time()
            for file, data in parser(rundowns):
                if data is None:
                    pbar.write(f"PROCESSING FILE FAILURE: {file}")
                else:
                    result[data.values()] = data
                    finish_time = time() - start_time
                    pbar.write(f"PROCESSING FILE SUCCESS: {file} in {finish_time} seconds.")
                # pbar.update(1)

        if parser.has_errors():
            logger.error(parser.errors)

        #
        # [2] Write CSV and XLSX files.
        #

        # TODO Report and remove empty lists from result data.
        df = pd.DataFrame([x for x in result.values() if len(x) > 0])

        with pd.ExcelWriter(output_file_path) as writer:
            df.to_excel(writer, sheet_name=f"SOURCE_W{week}", index=False, header = True)

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
