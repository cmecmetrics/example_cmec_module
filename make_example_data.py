""" make_test_data.py: download xWMT test dataset """

from pathlib import Path
import urllib.request
import sys

if __name__ == "__main__":

    model_path = Path(sys.argv[1])

    version = "20221005"
    flist = ["xwmt_input_example", "xwmt_obs_est_cmec"]

    for fname in flist:
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
