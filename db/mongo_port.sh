#!/bin/bash

export passwd=$MONGO_PASSWD
export db="scribbleDB"
export collect="layers"
export key="layer"

python3 mongo_port.py $db $collect $key $passwd
