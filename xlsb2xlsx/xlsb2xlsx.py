import os
import sys
import logging
import re
import glob
import tqdm
import argparse
import jpype
import asposecells

jpype.startJVM()
from asposecells.api import Workbook, LoadOptions

# Logging
logger = logging.getLogger(__name__)


def parse_args_fun(args):
    """Argument parser pulled out for modularity"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "xlsb_directory",
        default=None,
        help="path to directory containing .xlsb files to convert to .xlsx",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        default=False,
        action="store_true",
        help="Boolean flag to determine if the function should run recursively through child directories",
    )
    parser.add_argument(
        "--password",
        "-p",
        default=None,
        help="Password string",
    )
    input_args = parser.parse_args(args)
    return input_args


def glob_re(pattern, strings):
    """Function to incorporate regex into a glob file search"""
    return list(filter(re.compile(pattern, re.IGNORECASE).match, strings))


def convert_xlsb_to_xlsx(fp, password):
    """Wrapper of aspose-cells to convert .xlsb to .xlsx in existing directory"""
    print("Converting: " + fp + "...")
    options = LoadOptions()

    if password != None:
        options.setPassword(password)

    df = Workbook(fp, options)
    df.getSettings().setPassword(None)
    df.save(fp[:-5] + ".xlsx")


def run_xlsb2xlsx(arguments):
    if os.path.isdir(arguments.xlsb_directory):
        dir_path = arguments.xlsb_directory
    else:
        logger.error(
            "ERROR: The directory you have specified does not exist. Specify an existing directory in the 'xlsb_directory' argument and try again."
        )
        sys.exit(1)

    recursive = arguments.recursive

    # TODO: If a password was provided, we should probalby verify that it's correct instead of it throwing an error
    password = arguments.password

    if recursive == True:
        fps = glob_re(r".*\.xlsb", glob.glob(dir_path + "/**", recursive=True))
        print(f"RECURSIVELY Converting files in {dir_path}...")
    else:
        fps = glob_re(r".*\.xlsb", glob.glob(dir_path + "/**"))
        print(f"Converting files in {dir_path}...")

    print(f"\nProcessing {len(fps)} .xlsb files...")

    # Progress bar
    with tqdm.tqdm(total=len(fps)) as pbar:
        for filepath in fps:
            convert_xlsb_to_xlsx(filepath, password)
            pbar.update()
