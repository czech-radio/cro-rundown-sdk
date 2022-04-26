# -*- coding: utf-8 -*-

import argparse
import os
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from tqdm import tqdm

from cro.rundown.sdk._shared import failure_msg, success_msg

__all__ = tuple(["main", "inspect", "organize"])


load_dotenv()  # # Take environment variables from `.env`.


def main() -> None:
    """
    Arrange the rundown files in the given directory.
    """

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


def inspect(path: Path) -> Dict[date, List[Path]]:
    """
    For each file in the given directory read the last modified date
    and add them to the dictionary with the last modified date as a key and
    file path as the value.
    Only files in the given folder not in subfoldres are !
    Example:
        >>> _inspect(path)
        >>> Dict {
                "2020-01-12": [path, path, ..., path],
                "2020-02-12": [path, path, ..., path],
                ...
                "2020-31-12": [path, path, ..., path],
                "2021-01-01": [path, path, ..., path],
                ...
            }
    """
    rundowns: Dict[date, List[Path]] = {}
    for item in path.iterdir():
        if item.is_file():
            mtime = datetime.fromtimestamp(item.stat().st_mtime).date()
            if mtime in rundowns:
                rundowns[mtime].append(item)
            else:
                rundowns[mtime] = [item]

    return dict(sorted(rundowns.items()))


def organize(directory: Path, sorted_rundowns: Dict[date, List[Path]]) -> None:
    """
    Key is date e.g "2020-30-12" and items are file paths e.g
    [path1, path2, ...]
    """
    for key, items in sorted_rundowns.items():
        for item in tqdm(items):

            year_num, week_num, _ = key.isocalendar()

            if week_num > 9:
                week_str = f"{week_num}"
            else:  # prefix with zero.
                week_str = f"0{week_num}"

            week_path = directory / f"{year_num}" / f"W{week_str}"
            try:
                # When a path already exist, continue.
                week_path.mkdir(parents=True, exist_ok=False)
                status = f"SUCCESS: {week_path} created."
            except Exception as ex:
                status = f"WARNING: {week_path} existed."
            finally:
                pass  # REMOVE print(status)

            file_path = week_path / item.name
            try:
                # When a file already exist, continue.
                item.rename(file_path)
                status = f"SUCCESS: {file_path}"
            except Exception as ex:
                status = f"FAILURE: {file_path} | {ex}"
            finally:
                pass  # REMOVE print(status)
