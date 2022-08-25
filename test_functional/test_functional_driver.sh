#!/bin/bash

source $CONDA_SOURCE
conda activate $CONDA_ENV_ROOT/_CMEC_xwmt_env

python $CMEC_CODE_DIR/test_functional.py $CMEC_MODEL_DATA $CMEC_WK_DIR
