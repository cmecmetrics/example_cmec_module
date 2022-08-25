""" make_test_data.py: download xWMT test dataset """

from pathlib import Path
import urllib.request
import sys

if __name__ == "__main__":

    model_path = Path(sys.argv[1])
    data_path = model_path / "xwmt_test_data.nc"
    print(data_path)
    if not model_path.exists():
        model_path.mkdir(parents=True)
    if not data_path.exists():
        print("Downloading test data ...", end="")
        urllib.request.urlretrieve(
            "ftp://ftp.gfdl.noaa.gov/perm/John.Krasting/xwmt/xwmt_test_data.20220810.nc",
            data_path,
        )
        print("DONE!")
