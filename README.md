# Example CMEC Module  

This is an example of a CMEC module that complies with the CMEC-MDTF standard. The module is called "CMECTEST" and contains two configurations: C1 and C2.  

## Installation
Use git clone to obtain a local copy of this repository. Alternatively, to obtain a released version, go to the "Releases" section in the sidebar.

## Environment    
This module depends on numpy, xarray, netcdf4, and matplotlib along with other modules from the Python standard library. An environment called '_CMEC_test_env' must be created which includes these packages.

A yaml file is provided with the source code to help create this environment:  
`conda env create -f test_env.yaml`

## Create test data  
A script is provided to generate a test data file of approximately 1 Mb in size.   

The command is:  
`python make_test_data.py model_directory`  
"model_directory" can be the name of any existing directory. A file called "test_data_set.nc" will be written under that directory.  

## Register test module  
Activate an environment with cmec-driver installed.  

`cmec-driver register example_cmec_module/`  

## Run test module  
Activate an environment with cmec-driver installed.
If an output directory does not already exist, create one. Use the model_directory that contains the test data set.  

`cmec-driver run model_directory/ output/ CMECTEST`  

Navigate into the "output" folder to view the results. Each configuration will produce an html page that can be viewed in a browser.

## License
The CMEC example module is distributed under the terms of the BSD 3-Clause License.  

LLNL-CODE-831161
