# -*- coding: utf-8 -*-

import argparse
import sys
import xml.etree.ElementTree as ET
from os import stat
from pathlib import Path

from tqdm import tqdm

from cro.rundown.sdk._clean import clean_rundown as clean_rundown
from cro.rundown.sdk._clean import station_mapping
from cro.rundown.sdk._domain import Station
from cro.rundown.sdk._parse import parse_rundown as parse_rundown

__all__ = tuple(["main"])


def main():
    """
    1. Get a directory e.g `data/source` and list all XML files.
    2. Clean each XML file.
    3: Result write to the output folder e.g. `data/target`.

    Use batch or (async) stream?
    """
    try:
        parser = argparse.ArgumentParser(
            description="The rundown XML files cleaning and parsing."
        )

        parser.add_argument(
            "-v", "--version", action="store_true", help="The package version."
        )
        parser.add_argument(
            "-V", "--verbose", action="store_true", help="The verbose execution."
        )

        parser.add_argument(
            "-s", "--source", required=False, help="The source directory."
        )
        parser.add_argument(
            "-t", "--target", required=False, help="The target directory."
        )

        options = parser.parse_args()

        if options.help:
            parser.print_help()
            sys.exit(1)

        if options.version:
            from cro.rundown.sdk import __version__

            print(__version__)
            sys.exit(0)

        match options.source:
            case None:
                source_dir = Path("./data/source/")
            case _:
                source_dir = Path(options.source)

        match options.target:
            case None:
                target_dir = Path("./data/target/")
            case _:
                target_dir = Path(options.target)

        # (1)
        print("READING", end="")
        sources = [file for file in tqdm(source_dir.glob("*.xml"))]

        targets = {}

        for source in sources:
            hour, other = source.stem[3:8], source.stem[9:]

            station, date = other.split("-")

            date = tuple(date[1:-15][-21:-11].split("_"))
            hour = tuple(hour.split("-"))

            station = station.strip("_")  # Remove trailing `_`.
            station = station_mapping[station]  # Get station model.

            file_name = f"RUNDOWN_{date[2]}-{date[1]}-{date[0]}_{hour[0]}-{hour[1]}_{station.name}-{station.type.name}"

            print("CLEANING:", source, "==>", file_name)

            # (2)
            targets[file_name] = clean_rundown(tree=ET.parse(source))

        # (3)
        for name, tree in tqdm(targets.items()):
            tree.write(target_dir / f"{name}.xml", encoding="utf8")

        if verbose:
            print("Success")
            sys.exit(0)

    except Exception as ex:
        print(f"Failure: {ex}")
        raise ex
        sys.exit(1)
