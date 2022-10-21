""" make_test_data.py: download xWMT test dataset """

from pathlib import Path
import urllib.request
import sys

if __name__ == "__main__":

    model_path = Path(sys.argv[1])
    obs_path = Path(sys.argv[2]) / "xwmt"

    version = "20221005"
    mod_flist = ["xwmt_input_example"]
    obs_flist = ["xwmt_obs_est_cmec"]

    for fname in mod_flist:
        data_path = model_path / f"{fname}.tar.gz"
        if not model_path.exists():
            model_path.mkdir(parents=True)
        if not data_path.exists():
            print(f"Downloading {fname}.tar.gz ...", end="")
            sys.stdout.flush()
            urllib.request.urlretrieve(
                f"ftp://ftp.gfdl.noaa.gov/perm/John.Krasting/xwmt/{fname}.{version}.tar.gz",
                data_path,
            )
        print("DONE!")
    
    for fname in obs_flist:
        data_path = obs_path / f"{fname}.tar.gz"
        if not obs_path.exists():
            obs_path.mkdir(parents=True)
        if not data_path.exists():
            print(f"Downloading {fname}.tar.gz ...", end="")
            sys.stdout.flush()
            urllib.request.urlretrieve(
                f"ftp://ftp.gfdl.noaa.gov/perm/John.Krasting/xwmt/{fname}.{version}.tar.gz",
                data_path,
            )
        print("DONE!")
