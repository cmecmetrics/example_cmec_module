# xWMT CMEC Module

This CMEC runs the `xWMT` water mass transformation analysis. The module is called "XWMT" and contains a functional test configuration.  

## Installation
Use git clone to obtain a local copy of this repository. Alternatively, to obtain a released version, go to the "Releases" section in the sidebar.

The module is run via cmec-driver command line program ([code repository](https://github.com/cmecmetrics/cmec-driver)), which has its own [installation instructions](https://github.com/cmecmetrics/cmec-driver#installation).  

## Environment    
This module depends on the `xwmt` module. A conda environment called '_CMEC_xwmt_env' must be created which includes this package and its dependencies.

A yaml file is provided with the source code to help create this environment:  
`conda env create -f xwmt_env.yaml`

## Register xWMT CMEC modules  
Activate an environment with cmec-driver installed.  

`cmec-driver register path/to/cmec_xwmt/`  

## Example 1: Functional Tests
### Download test data  
A script is provided to download a test data file (approximately 214 MB in size).   

The command is:  
`python make_test_data.py model_directory`  
"model_directory" can be the name of any existing directory. A file called "xwmt_test_data.nc" will be written under that directory.  

### Run test module  
Activate an environment with cmec-driver installed.
If an output directory does not already exist, create one. Use the model_directory that contains the test data set from the "Create test data" section.  

`cmec-driver run model_directory/ output/ XWMT/test_functional`  

Navigate into the "output" folder to view the results. Each configuration will produce an html page that can be viewed in a browser.

## Example 2: Full Surface WMT Example
### Download Model Data 
A sample dataset containing 5 years of GFDL CM4 output along with processed ECCO and ERA5 reanalysis data for comparison is also available.

A script is provided to download example data (aproximately 720 MB in size).   

The command is:  
`python make_example_data.py model_directory obs_directory`  
"model_directory" and "obs_directory" can be the name of any existing directorys. Two compressed tar files will be written under these directories.

After downloading, unpack the tar files:

```
cd model_directory
tar -xzvf xwmt_input_example.tar.gz
cd ../

cd obs_directory/xwmt
tar -xzvf xwmt_obs_est_cmec.tar.gz
cd ../../
```

To save disk space, the tars file can be deleted once the files are unpacked

A sample figue of the output is also provided in the `extra_resources` directory

### Run test module  
Activate an environment with cmec-driver installed.
If an output directory does not already exist, create one. Use the model_directory and obs_directory that contain the data downloaded from the previous section.  

`cmec-driver run --obs obs_directory model_directory/ output/ XWMT/full_example`  

Navigate into the "output" folder to view the results. Each configuration will produce an html page that can be viewed in a browser.

## License
The xwmt CMEC module is distributed under the terms of the BSD 3-Clause License.  
LLNL-CODE-831161

## Acknowledgments
This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory (LLNL) under Contract DE-AC52-07NA27344. It is a contribution to the science portfolio of the U.S. Department of Energy, Office of Science, Earth and Environmental Systems Sciences Division, Regional and Global Model Analysis Program.
