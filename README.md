# xWMT CMEC Module

This CMEC runs the `xWMT` water mass transformation analysis. The module is called "XWMT" and contains a functional test configuration.  

## Installation
Use git clone to obtain a local copy of this repository. Alternatively, to obtain a released version, go to the "Releases" section in the sidebar.

The module is run via cmec-driver command line program ([code repository](https://github.com/cmecmetrics/cmec-driver)), which has its own [installation instructions](https://github.com/cmecmetrics/cmec-driver#installation).  

## Environment    
This module depends on the `xwmt` module. A conda environment called '_CMEC_xwmt_env' must be created which includes this package and its dependencies.

A yaml file is provided with the source code to help create this environment:  
`conda env create -f xwmt_env.yaml`

## Download test data  
A script is provided to download a test data file of approximately 214 Mb in size.   

The command is:  
`python make_test_data.py model_directory`  
"model_directory" can be the name of any existing directory. A file called "xwmt_test_data.nc" will be written under that directory.  

## Register test module  
Activate an environment with cmec-driver installed.  

`cmec-driver register path/to/cmec_xwmt/`  

## Run test module  
Activate an environment with cmec-driver installed.
If an output directory does not already exist, create one. Use the model_directory that contains the test data set from the "Create test data" section.  

`cmec-driver run model_directory/ output/ XWMT/test_functional`  

Navigate into the "output" folder to view the results. Each configuration will produce an html page that can be viewed in a browser.

## License
The xwmt CMEC module is distributed under the terms of the BSD 3-Clause License.  

LLNL-CODE-831161
