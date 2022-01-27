"""
This script creates a fake dataset of roughly 1 mb in size.
The data is a 1x1 lat/lon grid populated with values of "1".
The dimensions are lat x lon x time.
"""
import json
import numpy as np
from pathlib import Path
import sys
import xarray as xr

if __name__ == "__main__":
    """Create fake model data."""

    model_path = Path(sys.argv[1])
    data_path = model_path / "test_data_set.nc"
    if not model_path.exists():
        model_path.mkdir(parents=True)
    if not data_path.exists():
        lat = np.linspace(-90,90,180)
        lon = np.linspace(0,360,360,endpoint=False)
        time = np.linspace(0,2,2)
        coordinates = {'lat':lat,'lon':lon,'time':time}
        rand_data = np.ones((180, 360, 2))
        new_array = xr.Dataset(
            data_vars=dict(test_var=(['lat','lon','time'], rand_data)),
            coords=coordinates,attrs=dict(description="fake data for test"))
        new_array.to_netcdf(str(data_path), mode="w")

