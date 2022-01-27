# Example CMEC Module  

This is an example of a CMEC module that complies with the CMEC-MDTF standard. The module is called "CMECTEST" and contains two configurations: C1 and C2.  

## Environment:  
This module depends on numpy, xarray, netcdf4, and matplotlib along with other modules from the Python standard library.  

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
