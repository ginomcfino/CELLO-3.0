#!/bin/bash

# create and activate virtual environment
# python3 -m venv env
# source env/bin/activate

# check if brew is installed, and install if necessary
if ! command -v brew &> /dev/null
then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# install redis using brew
brew install redis

# install required Python packages
pip install redis dash dash-core-components dash-html-components requests
