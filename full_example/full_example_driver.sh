#!/bin/bash

source $CONDA_SOURCE
conda activate $CONDA_ENV_ROOT/_CMEC_xwmt_env

python $CMEC_CODE_DIR/full_example.py $CMEC_OBS_DATA $CMEC_MODEL_DATA $CMEC_WK_DIR
