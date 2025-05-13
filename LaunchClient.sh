#!/bin/bash

if [ -z "$1" ]; then
    echo "Erreut: IP manquante"
    echo "Usage: $0 <IP_ADDRESS>"
    exit 1
fi


IP_ADDRESS=$1

QTABLE_FILENAME="$2"

source ./myenv/bin/activate

if [ -n "$QTABLE_FILENAME" ]; then
    python3 qlearn.py --ip "$IP_ADDRESS" --qtable "$QTABLE_FILENAME"
else
    python3 qlearn.py --ip "$IP_ADDRESS"
fi

deactivate
