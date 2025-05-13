#!/bin/bash

source ./myenv/bin/activate

nohup python3 ./server.py > output.log 2>&1 &
python3 capteur.py

deactivate
