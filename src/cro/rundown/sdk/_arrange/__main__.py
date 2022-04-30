# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

from cro.rundown.sdk import inspect, organize
from cro.rundown.sdk._shared import failure_msg, success_msg


def main() -> None:
    """
    Arrange the rundown files in the given directory.
    """

    load_dotenv()  # Take environment variables from `.env`.

    parser = argparse.ArgumentParser(description="The `cro.rundown.arrange` program.")

    parser.add_argument(
        "-s", "--source", required=False, help="The rundown source directory path."
    )

    options = parser.parse_args()

    match options.source:
        case None:
            source = Path(os.getenv("RUNDOWN_EXPORT_PATH"))
        case _:
            source: str = Path(options.source)

    try:
        sorted_rundowns = inspect(source)
        print(f"PREPARE: Rundown {len(sorted_rundowns.values())}")
        organize(source, sorted_rundowns)
        print(success_msg(f"Rundowns {len(sorted_rundowns.items())} processed"))

    except Exception as ex:

        print(failure_msg(ex))
