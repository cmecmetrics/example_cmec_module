# Example CMEC Module  

This is an example of a CMEC module that complies with the CMEC-MDTF standard. The module is called "CMECTEST" and contains two configurations: C1 and C2.  

## Installation
The [CMEC Module Manager](https://github.com/cmecmetrics/cmec-module-man) can be used to install this module with the following command:  
`python setup_module.py CMECTEST`  

Another option is to use git clone to obtain a local copy of this repository. Alternatively, to obtain a released version, go to the "Releases" section in the sidebar.

The module is run via cmec-driver command line program ([code repository](https://github.com/cmecmetrics/cmec-driver)), which has its own [installation instructions](https://github.com/cmecmetrics/cmec-driver#installation).  

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

`cmec-driver register path/to/example_cmec_module/`  

## Run test module  
Activate an environment with cmec-driver installed.
If an output directory does not already exist, create one. Use the model_directory that contains the test data set from the "Create test data" section.  

`cmec-driver run model_directory/ output/ CMECTEST/C1 CMECTEST/C2`  

Navigate into the "output" folder to view the results. Each configuration will produce an html page that can be viewed in a browser.  

## For developers  
Please note that the following files are not required CMEC files: "LICENSE", "NOTICE".  

If forking this repository to use as a template for a future module, you may with to "detach" your fork from the example_cmec_repository. For help, see [GitHub Support](https://support.github.com/request/fork).  

## License
The CMEC example module is distributed under the terms of the BSD 3-Clause License.  
LLNL-CODE-831161

## Acknowledgement
Content in this repository is developed by climate and computer scientists from the Program for Climate Model Diagnosis and Intercomparison ([PCMDI][PCMDI]) at Lawrence Livermore National Laboratory ([LLNL][LLNL]). This work is sponsored by the Regional and Global Model Analysis ([RGMA][RGMA]) program, of the Earth and Environmental Systems Sciences Division ([EESSD][EESSD]) in the Office of Biological and Environmental Research ([BER][BER]) within the [Department of Energy][DOE]'s [Office of Science][OS]. The work is performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.  

[PCMDI]: https://pcmdi.llnl.gov/
[LLNL]: https://www.llnl.gov/
[RGMA]: https://climatemodeling.science.energy.gov/program/regional-global-model-analysis
[EESSD]: https://science.osti.gov/ber/Research/eessd
[BER]: https://science.osti.gov/ber
[DOE]: https://www.energy.gov/
[OS]: https://science.osti.gov/

<p>
    <img src="https://github.com/PCMDI/assets/blob/main/DOE/480px-DOE_Seal_Color.png?raw=true"
         width="65"
         style="margin-right: 30px"
         title="United States Department of Energy"
         alt="United States Department of Energy"
    >&nbsp;
    <img src="https://github.com/PCMDI/assets/blob/main/LLNL/212px-LLNLiconPMS286-WHITEBACKGROUND.png?raw=true"
         width="65"
         title="Lawrence Livermore National Laboratory"
         alt="Lawrence Livermore National Laboratory"
    >
</p>
