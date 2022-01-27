import argparse
from datetime import datetime, timezone
import logging
import json
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
    
def write_json(data,filename):
    """Create a new JSON file.
    Args:
        data (dictionary): data to write
        filename (str): output file name
    """
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4)

def weighted_mean(input_data_path, var):
    """Returns the temporal and spatial weighted mean for a variable.

    Args:
        input_data_path (str): path to the input netCDF
        var (str): name of the variable to average
    """
    data = xr.load_dataset(input_data_path)
    data_weights = np.cos(np.deg2rad(data.lat))
    data_weights.name = "weights"
    weighted_data = data.weighted(data_weights)
    weighted_mean = weighted_data.mean(("time","lon","lat"))
    return float(weighted_mean[var].data)

if __name__ == "__main__":
    """Example of a module script that calculates a metric and generates
    a CMEC-compliant metrics JSON and metadata file.
    """
    parser = argparse.ArgumentParser(description="inputs for weighted mean")
    parser.add_argument("input", help="netCDF data path")
    parser.add_argument("var", help="variable name to average")
    parser.add_argument("output", help="output directory")
    args = parser.parse_args()
    
    log_file_name = Path(args.output)/"config1.log"
    logging.basicConfig(filename=str(log_file_name), encoding="utf-8", level=logging.INFO)

    # Calculate metric
    logging.info("Calculating metric")
    weighted_average = weighted_mean(args.input, args.var)
    
    # Write metric to file
    current_date = datetime.now(timezone.utc).strftime("%b %d %Y %H:%M:%S")+" UTC"

    metrics_json = {"SCHEMA": {}, "DIMENSIONS": {}, "RESULTS": {"Global": {}}}
    metrics_json["SCHEMA"] = {"name": "CMEC", "version": "v1", "package": "CMECTEST"}
    metrics_json["DIMENSIONS"]["json_structure"] = ["region", "var", "metric"]
    metrics_json["DIMENSIONS"]["metric"] = {"weighted_mean": {"Name": "Spatially weighted mean", "Contact": "none"}}
    metrics_json["DIMENSIONS"]["region"] = {"Global": {}}
    metrics_json["PROVENANCE"] = {
        "date": current_date,
        "environment": get_package_versions()}
    metrics_json["RESULTS"]["Global"][args.var] = {}
    metrics_json["RESULTS"]["Global"][args.var]["weighted_mean"] = weighted_average
    
    metrics_base_name = "weighted_mean.json"
    metrics_file_name = Path(args.output)/metrics_base_name
    write_json(metrics_json, metrics_file_name)
    
    # Write html page
    logging.info("Writing index.html")
    html_text = [
            "<html>\n<head><title>Test page 1</title></head>\n",
            "<h1>Metrics</h1>\n",
            "<p><a href={0}>Link to metrics</a></p></html>".format(metrics_base_name)]
    index_file_name = Path(args.output)/"index.html"
    with open(index_file_name, "w") as index_html:
        index_html.writelines(html_text)
    
    # Write output bundle metadata
    logging.info("Writing metadata file")
    meta_json = {}
    meta_json["index"] = "index.html"
    meta_json["provenance"] = {
        "environment": get_package_versions(),
        "modeldata": args.input,
        "obsdata": None,
        "log": "config1.log",
        "date": current_date}
    meta_json["metrics"] = {
        "filename": metrics_base_name,
        "long_name": "metrics",
        "description": "Weighted mean of dataset"
    }
    
    output_file_name = Path(args.output)/"output.json"
    write_json(meta_json, output_file_name)
    