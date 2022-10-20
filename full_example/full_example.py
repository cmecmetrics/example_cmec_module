import argparse
import logging
from pathlib import Path
import numpy as np
import xarray as xr
import glob
import os
from xwmt.swmt import swmt
import matplotlib.pyplot as plt

#

import pkg_resources as pkgr
import pytest

# lambda (lstr) space
lstr = "sigma0"  # sigma0, theta, salt
subdir = "GFDL-CM4_historical"
# Select spatial domain (global or basin name)
basin_name = "pacific_tropc"  # global, atlantic, indian, pacific, southern, arctic,

# Set boundaries and bin sizes
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


def read(args):
    rootdir = args.input

    # Directory to save wmt output file (change accordingly)
    # Model dataset used for this example (change accordingly)
    # Path for the corresponding WMT datasets generated from ECCOv4 and ERA5 reanalysis
    dset_dir = f"{args.obs}/xwmt/obs_est_cmec/data"

    variables = ["tos", "sos", "hfds", "wfo", "sfdsi"]
    variables_static = ["areacello", "deptho", "basin"]

    # For atlantic and pacific you can add _tropc, _subtN, _subpN, _subtS (e.g., atlantic_subpN, pacific_tropc)
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

    ## Loading reanalysis data
    # Select the same time range as the model data
    yr_st = str(ds.time.dt.year[0].values)
    yr_ed = str(ds.time.dt.year[-1].values)

    ddict = {}
    for dset in ["ecco.ecco", "era5.en4"]:
        # filepath = os.path.join(dset_dir,dset.split('.')[0])
        filename = "-".join([dset + ".G", lstr, basin_name]) + ".nc"
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
    # Subsample spatial domain
    bidx = [item.split("_")[0] for item in ds.basin.flag_meanings.split(" ")].index(
        basin_name.split("_")[0]
    )

    if basin_name == "global":
        mask = xr.where(ds.basin == bidx, 0, 1)
    else:
        mask = ds.basin == bidx

    if basin_name[-6:] == "_tropc":
        mask = mask & (ds["lat"] <= 20) & (ds["lat"] >= -20)
    if basin_name[-6:] == "_subtN":
        mask = mask & (ds["lat"] <= 45) & (ds["lat"] > 20)
    if basin_name[-6:] == "_subpN":
        mask = mask & (ds["lat"] > 45)
    if basin_name[-6:] == "_subtS":
        mask = mask & (ds["lat"] >= -45) & (ds["lat"] < -20)

    # Use xwmt to calculate the surface water mass transformation for given domain
    G = swmt(ds.where(mask)).G(lstr, bins=np.arange(lmin, lmax, dl), group_tend=False)

    # Safe output to netcdf file
    fname = (
        "_".join(
            [
                subdir + ".G",
                "%sto%s"
                % (
                    str(G.time.dt.year[0].values).rjust(4, "0"),
                    str(G.time.dt.year[-1].values).rjust(4, "0"),
                ),
                lstr,
                basin_name,
            ]
        )
        + ".nc"
    )
    # Add attributes?
    print("Saving to file:", fname)
    G.reset_coords(drop=True).to_netcdf(args.output + fname, format="NETCDF4")

    # Load dataset from file
    G = xr.open_dataset(args.output + fname)

    # Calculate total from thermal and haline components
    da = xr.zeros_like(G[list(G.keys())[0]]).rename("total")
    for tend in G.keys():
        da += G[tend]
    G["total"] = da

    return G


def plot(G, ddict, yr_st, yr_ed):

    # Safe output to netcdf file
    fname = (
        "_".join(
            [
                subdir + ".G",
                "%sto%s"
                % (
                    str(G.time.dt.year[0].values).rjust(4, "0"),
                    str(G.time.dt.year[-1].values).rjust(4, "0"),
                ),
                lstr,
                basin_name,
            ]
        )
        + ".nc"
    )

    # Generate comparison figure
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(14, 8))

    for i, ten in enumerate(G.keys()):
        axs[i].axhline(y=0, xmin=0, xmax=1, linewidth=1.0, color="k")
        axs[i].plot(
            G[lstr], G.mean("time")[ten] * 1e-6, c="k", lw=3, ls="-", label=subdir
        )
        for dset in ddict:
            axs[i].plot(
                ddict[dset][lstr],
                ddict[dset][ten] * 1e-6,
                lw=2,
                linestyle="-",
                label=dset.upper(),
            )
        axs[i].set_ylabel("WMT [Sv]", fontsize=14)
        axs[i].set_title(ten, fontsize=14)
        if i == 0:
            axs[i].legend(loc="lower left", ncol=3, fontsize=12)

    fig.suptitle(basin_name.capitalize() + " (%s-%s)" % (yr_st, yr_ed), fontsize=18)
    print("Saving figure to file:", fname.replace(".nc", "_comparison.png"))
    plt.savefig(
        args.output + fname.replace(".nc", "_comparison.png"),
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

    parser = argparse.ArgumentParser(description="inputs for xwmt full example")
    parser.add_argument("obs", help="observational data path")
    parser.add_argument("input", help="model netCDF data path")
    parser.add_argument("output", help="output directory")
    args = parser.parse_args()

    log_file_name = Path(args.output) / "xwmt_full_example.log"
    logging.basicConfig(
        filename=str(log_file_name), encoding="utf-8", level=logging.INFO
    )

    logging.info("Running xwmt full example")
    os.chdir(args.input)
    print("Hello world!", os.getcwd())

    ds, ddict, yr_st, yr_ed = read(args)
    G = calculate(ds)
    plot(G, ddict, yr_st, yr_ed)
