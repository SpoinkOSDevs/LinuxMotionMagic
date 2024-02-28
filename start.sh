#!/bin/bash

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the "Engine" directory
cd "$DIR/Engine"

# Run the Python script
python3 Core.py

