# -*- coding: utf-8 -*-


import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from tqdm import tqdm

from cro.rundown.sdk import clean_rundown_content, clean_rundown_name
from cro.rundown.sdk._shared import failure_msg, success_msg


def main():
    """The main CLI function to clean the specified rundowns.

    1. Get a directory e.g `data/source` and list all XML files.
    2. Clean each XML file.
    3: Result write to the output folder e.g. `data/target`.

    Use batch or (async) stream?
    """

    parser = argparse.ArgumentParser(description="The `cro.rundown.cleanse` program.")

    parser.add_argument(
        "-v",
        "--version",
        required=False,
        action="store_true",
        help="The package version.",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        required=False,
        action="store_true",
        help="The verbose execution.",
    )

    parser.add_argument("-s", "--source", required=False, help="The source directory.")
    parser.add_argument("-t", "--target", required=False, help="The target directory.")

    options = parser.parse_args()

    verbose = options.verbose

    # if options.usage:
    #     parser.print_usage() # ? print_help()
    #     sys.exit(0)

    if options.version:
        from cro.rundown.sdk import __version__

        print(__version__)
        sys.exit(0)

    match options.source:
        case None:  # Default source directory?
            source_dir = Path("./data/source/")
        case _:
            source_dir = Path(options.source)

    match options.target:
        case None:  # Default target directory?
            target_dir = Path("./data/target/")
        case _:
            target_dir = Path(options.target)

    # Read files for processing.
    sources = [file for file in tqdm(source_dir.glob("**/*.xml"))]
    # TODO Sort the by ?
    # TODO Create them to batch of size ?

    try:
        targets = {}
        processed_files = []

        # Process the files.
        for source in sources:
            processed_files.append(source)
            year, file_name = clean_rundown_name(source)
            print(f"CLEANING {len(processed_files)}/{len(sources)}:  ==> {file_name}")
            targets[file_name] = clean_rundown_content(tree=ET.parse(source))

            # Save the processed file on each iteration.
            tree, name = targets[file_name], file_name

            path = target_dir / year / f"{name}.xml"

            with open(path, mode="wb+") as file:
                tree.write(file, encoding="utf-8")

        # Save the processed files after processing.
        # for name, tree in tqdm(targets.items()):
        # tree.write(target_dir / year / f"{name}.xml", encoding="utf8")

        if verbose:
            print(success_msg())
            sys.exit(0)

        # TODO Dump a processed files statistics as CSV:
        # `source file name`, `target file name`

    except Exception as ex:
        print(f"Failure: {str(ex)}, {processed_files[-1]}")
        # TODO Dump all succesfully processed files (CSV) to be
        # able to skip them in another run.
        raise ex  # sys.exit(1)
