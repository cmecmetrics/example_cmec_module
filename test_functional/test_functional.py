""" test_functional.py: XWMT test configuration """


import argparse
import logging
import os
from pathlib import Path

import pkg_resources as pkgr
import pytest

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="inputs for xwmt functional tests")
    parser.add_argument("input", help="netCDF data path")
    parser.add_argument("output", help="output directory")
    args = parser.parse_args()

    log_file_name = Path(args.output) / "config1.log"
    logging.basicConfig(
        filename=str(log_file_name), encoding="utf-8", level=logging.INFO
    )

    logging.info("Running functional tests")
    os.chdir(args.input)
    pytest.main([pkgr.resource_filename("xwmt", "tests/")])
