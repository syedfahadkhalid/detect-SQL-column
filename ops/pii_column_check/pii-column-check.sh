#!/bin/bash -xe

pip3 install -r ./ops/pii_column_check/requirements.txt --user

OUTPUT=$(python3 ./ops/pii_column_check/main.py --commit_id=$COMMIT_ID)

eval $OUTPUT