#!/bin/bash

python $CMEC_CODE_DIR/calculate_weighted_mean.py \
$CMEC_MODEL_DATA/test_data_set.nc test_var \
$CMEC_WK_DIR
