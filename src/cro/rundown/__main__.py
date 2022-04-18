# -*- coding: utf-8 -*-

from os import stat
import sys
import argparse
import xml.etree.ElementTree as ET

from pathlib import Path

from tqdm import tqdm

from cro.rundown._parse import parse_rundown as parse_rundown
from cro.rundown._clean import clean_rundown as clean_rundown, station_mapping

from cro.rundown._domain import Station


__all__ = tuple(["main"])


def main():
    """
    - 1. Get a directory e.g `data/source` and list all XML files.
    - 2. Clean each XML file.
    - 3: Result write to the output folder e.g. `data/target`.

    ? batch vs async stream
    """
    try:
        parser = argparse.ArgumentParser(description="The rundown XML files cleaning and parsing.")

        parser.add_argument("-v", "--version", help="The package version.")
        parser.add_argument("-V", "--verbose", action='store_true', help="The verbose execution.")

        parser.add_argument("-s", "--source", required=False, help="The source directory.")
        parser.add_argument("-t", "--target", required=False, help="The target directory.")

        options = parser.parse_args()

        verbose = options.verbose

        match options.source:
            case None:
                source_dir = Path("./data/source/")
            case _:
                source_dir = Path(options.source)

        match options.target:
            case None:
                target_dir =Path("./data/target/")
            case _:
                target_dir = Path(options.target)

        # (1)
        print("READING", end="")
        sources = [file for file in tqdm(source_dir.glob("*.xml"))]

        targets = { }

        for source in sources:
            hour, other= source.stem[3:8], source.stem[9:]

            station, date = other.split("-")

            date = tuple(date[1:-15][-21:-11].split("_"))
            hour = tuple(hour.split("-"))

            station = station.strip("_")       # Remove trailing `_`.
            station = station_mapping[station] # Get station model.

            file_name = f"RUNDOWN_{date[2]}-{date[1]}-{date[0]}_{hour[0]}-{hour[1]}_{station.name}-{station.type.name}"

            print("CLEANING:", source, "==>", file_name)

            # (2)
            targets[file_name] =  clean_rundown(tree = ET.parse(source))


        # (3)
        for name, tree in tqdm(targets.items()):
            tree.write(target_dir / f"{name}.xml", encoding="utf8")

        if verbose: print("Success"); sys.exit(0)

    except Exception as ex:
        print(f"Failure: {ex}"); raise ex
        sys.exit(1)
