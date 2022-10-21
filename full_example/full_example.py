""" full_example.py: surface watermass transformation example for CMEC """

import argparse
import glob
import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from xwmt.swmt import swmt


def _bin_boundaries(lstr="sigma0"):
    """sets boundaries and bin sizes"""
    if lstr == "sigma0":
        lmin = 10
        lmax = 30
        dl = 0.1
    elif lstr == "theta":
        lmin = -2
        lmax = 30
        dl = 0.5
    elif lstr == "salt":
        lmin = 20
        lmax = 40
        dl = 0.1

    return (lmin, lmax, dl)


def read(args):
    """Read model and reanalysis data"""

    rootdir = args.input

    # Path for the corresponding WMT datasets generated from ECCOv4 and ERA5 reanalysis
    dset_dir = f"{args.obs}/xwmt/obs_est_cmec/data"

    # List of input variables, and time-invariant static fields
    variables = ["tos", "sos", "hfds", "wfo", "sfdsi"]
    variables_static = ["areacello", "deptho", "basin"]

    # Load relevant variables for surface WMT
    ds = xr.Dataset()
    for var in variables:
        file_string = f"{args.input}/{var}*.nc"
        if glob.glob(file_string):
            print("Loading", file_string)
            ds[var] = xr.open_mfdataset(file_string, use_cftime=True)[var]
        else:
            print("Warning: No files available for", var)

    # Load static grid files
    grid = []
    for var in variables_static:
        file_string = f"{args.input}/{var}*.nc"
        if glob.glob(file_string):
            print("Loading", file_string)
            grid.append(xr.open_mfdataset(file_string, use_cftime=True))
        else:
            print("Warning: No files available for", var)

    # Combine variables with static grid info
    ds = xr.merge([ds, xr.merge(grid[1:])])

    # Note: areacello needs to be added seperately after renaming MOM6-specific dimension names (xh, yh)
    ds["areacello"] = grid[0].areacello.rename({"xh": "x", "yh": "y"})

    # Create land mask "wet" from deptho
    ds["wet"] = xr.where(~np.isnan(ds.deptho), 1, 0)
    # wet is 1 for ocean and 0 for land

    # Create an all-zero data array for sfdsi (when it is missing)
    if not "sfdsi" in ds:
        print("sfdsi is missing: Add all-zero field for sfdsi based on hfds")
        ds["sfdsi"] = xr.zeros_like(ds["hfds"]).rename("sfdsi")
        # Remove all attributes
        ds["sfdsi"].attrs = {}

    # Loading reanalysis at the same time range as the model data
    yr_st = str(ds.time.dt.year[0].values)
    yr_ed = str(ds.time.dt.year[-1].values)

    # Create a dictionary to hold the precalculated reanalysis output
    ddict = {}
    for dset in ["ecco.ecco", "era5.en4"]:
        # filepath = os.path.join(dset_dir,dset.split('.')[0])
        filename = "-".join([dset + ".G", args.lstr, args.basin]) + ".nc"
        print("Loading", filename)
        dset_ds = xr.open_dataset(dset_dir + "/" + filename).sel(
            time=slice(yr_st, yr_ed)
        )

        da = xr.zeros_like(dset_ds[list(dset_ds.keys())[0]]).rename("total")
        for tend in dset_ds.keys():
            da += dset_ds[tend]

        dset_ds["total"] = da
        ddict[dset.split(".")[0]] = dset_ds.mean("time")

    return (ds, ddict, yr_st, yr_ed)


def calculate(ds):
    """Performs the surface WMT analysis on the mode dataset, ds"""

    # Subsample spatial domain
    bidx = [item.split("_")[0] for item in ds.basin.flag_meanings.split(" ")].index(
        args.basin.split("_")[0]
    )

    # Setup masks for requested region
    if args.basin == "global":
        mask = xr.where(ds.basin == bidx, 0, 1)
    else:
        mask = ds.basin == bidx

    if args.basin[-6:] == "_tropc":
        mask = mask & (ds["lat"] <= 20) & (ds["lat"] >= -20)
    if args.basin[-6:] == "_subtN":
        mask = mask & (ds["lat"] <= 45) & (ds["lat"] > 20)
    if args.basin[-6:] == "_subpN":
        mask = mask & (ds["lat"] > 45)
    if args.basin[-6:] == "_subtS":
        mask = mask & (ds["lat"] >= -45) & (ds["lat"] < -20)

    # Get bin boundaries based on choice of lambda
    lmin, lmax, dl = _bin_boundaries(args.lstr)

    # Use xwmt to calculate the surface water mass transformation for given domain
    G = swmt(ds.where(mask)).G(
        args.lstr, bins=np.arange(lmin, lmax, dl), group_tend=False
    )

    # Save wmt output to netcdf file
    fname = (
        "_".join(
            [
                args.label + ".G",
                "%sto%s"
                % (
                    str(G.time.dt.year[0].values).rjust(4, "0"),
                    str(G.time.dt.year[-1].values).rjust(4, "0"),
                ),
                args.lstr,
                args.basin,
            ]
        )
        + ".nc"
    )

    print("Saving to file:", fname)
    G.reset_coords(drop=True).to_netcdf(args.output + "/" + fname, format="NETCDF4")

    # Load dataset from file
    G = xr.open_dataset(args.output + "/" + fname)

    # Calculate total from thermal and haline components
    da = xr.zeros_like(G[list(G.keys())[0]]).rename("total")
    for tend in G.keys():
        da += G[tend]
    G["total"] = da

    return G


def plot(G, ddict, yr_st, yr_ed):
    """Plots the model results along with reanalysis products"""

    # Generate comparison figure
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(14, 8))

    for i, ten in enumerate(G.keys()):
        axs[i].axhline(y=0, xmin=0, xmax=1, linewidth=1.0, color="k")
        axs[i].plot(
            G[args.lstr],
            G.mean("time")[ten] * 1e-6,
            c="k",
            lw=3,
            ls="-",
            label=args.label,
        )
        for dset in ddict:
            axs[i].plot(
                ddict[dset][args.lstr],
                ddict[dset][ten] * 1e-6,
                lw=2,
                linestyle="-",
                label=dset.upper(),
            )
        axs[i].set_ylabel("WMT [Sv]", fontsize=14)
        axs[i].set_title(ten, fontsize=14)
        if i == 0:
            axs[i].legend(loc="lower left", ncol=3, fontsize=12)

    fig.suptitle(args.basin.capitalize() + " (%s-%s)" % (yr_st, yr_ed), fontsize=18)

    # Setup output name
    fname = (
        "_".join(
            [
                args.label + ".G",
                "%sto%s"
                % (
                    str(G.time.dt.year[0].values).rjust(4, "0"),
                    str(G.time.dt.year[-1].values).rjust(4, "0"),
                ),
                args.lstr,
                args.basin,
            ]
        )
        + ".nc"
    )

    # Save the figure
    print("Saving figure to file:", fname.replace(".nc", "_comparison.png"))
    plt.savefig(
        args.output + "/" + fname.replace(".nc", "_comparison.png"),
        dpi=None,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
        format="png",
        transparent=False,
        bbox_inches="tight",
        pad_inches=0.1,
    )


if __name__ == "__main__":
    """Main run function"""

    # required runtime parameters
    parser = argparse.ArgumentParser(description="inputs for xwmt full example")
    parser.add_argument("obs", help="observational data path")
    parser.add_argument("input", help="model netCDF data path")
    parser.add_argument("output", help="output directory")

    # optional arguments
    parser.add_argument(
        "--label", type=str, default="model", help="label string for model/experiemnt"
    )
    parser.add_argument(
        "--lstr",
        type=str,
        default="sigma0",
        help="lambda space ('sigma0', 'theta', or 'salt')",
    )
    parser.add_argument(
        "--basin",
        type=str,
        default="pacific_tropc",
        help="lambda space ('pacific_tropc', 'global', 'atlantic', 'indian', 'pacific', 'southern', 'arctic'",
    )

    # resolve all arguments
    args = parser.parse_args()

    # setup logging
    log_file_name = Path(args.output) / "xwmt_full_example.log"
    logging.basicConfig(
        filename=str(log_file_name), encoding="utf-8", level=logging.INFO
    )

    # change to model input directory
    logging.info("Running xwmt full example")
    os.chdir(args.input)

    # separte functions to read data, calculate wmt, and plot results
    ds, ddict, yr_st, yr_ed = read(args)
    G = calculate(ds)
    plot(G, ddict, yr_st, yr_ed)
