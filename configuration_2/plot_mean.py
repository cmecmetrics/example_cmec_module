import argparse
from datetime import datetime, timezone
import json
import logging
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import platform
import xarray as xr

def get_package_versions():
    """Return versions of key python packages."""
    versions = {}
    versions["numpy"] = np.__version__
    versions["xarray"] = xr.__version__
    versions["python"] = platform.python_version()
    return versions

def make_plot(input_data_path, output_plot_path):
    """Returns the temporal and spatial weighted mean for a variable

    Args:
        input_data_path (str): path to the input netCDF
        output_plot_path (str): file name of output figure
    """
    data = xr.load_dataset(input_data_path)
    time_mean = data.mean("time")
    time_mean.test_var.plot()
    plt.savefig(output_plot_path)
    return

if __name__ == "__main__":
    """Example of a module script that creates a figure and generates
    a CMEC-compliant metrics JSON and metadata file.
    """
    parser = argparse.ArgumentParser(description="inputs for weighted mean")
    parser.add_argument("input", help="netCDF data path")
    parser.add_argument("var", help="variable name to average")
    parser.add_argument("output", help="output directory")
    args = parser.parse_args()
    
    log_file_name = Path(args.output)/"config2.log"
    logging.basicConfig(filename=str(log_file_name), encoding="utf-8", level=logging.INFO)
    
    # Calculate metric
    logging.info("Generating plot")
    output_plot_name = Path(args.output)/"plot.png"
    make_plot(args.input,output_plot_name)
    
    # Write html page
    logging.info("Writing index.html")
    index_file_name = Path(args.output)/"index.html"
    with open(index_file_name, "w") as index_html:
        index_html.writelines([
            '<html>\n<head><title>Test page 2</title></head>\n',
            '<h1>Figure</h1>\n',
            '<p><img src="plot.png",alt="example map"></p></html>'])
    
    # Write output bundle metadata
    logging.info("Writing metadata file")
    current_date = datetime.now(timezone.utc).strftime("%b %d %Y %H:%M:%S")+" UTC"
    
    meta_json = {}
    meta_json["index"] = "index.html"
    meta_json["provenance"] = {
        "environment": get_package_versions(),
        "modeldata": args.input,
        "obsdata": None,
        "log": "config2.log",
        "date": current_date}
    meta_json["plots"] = {
        "filename": "plot.png",
        "long_name": "Test map",
        "description": "Map of the test dataset"
    }

    output_file_name = Path(args.output)/"output.json"
    with open(output_file_name, "w") as outfile:
        json.dump(meta_json, outfile, indent=4)
    