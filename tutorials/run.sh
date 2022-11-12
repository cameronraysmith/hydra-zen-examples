#!/usr/bin/env bash

export PYTHON_TRACE_IGNORE=$(python -c 'import sys ; print(":".join(sys.path)[1:])')
python -m trace --trace --ignore-dir=$PYTHON_TRACE_IGNORE my_app.py player.name=frodo