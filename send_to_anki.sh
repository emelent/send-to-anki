#!/bin/bash

(
    cd /Users/roy/Code/python/anki/
    source .venv/bin/activate
    python3 main.py $*
    deactivate
)
