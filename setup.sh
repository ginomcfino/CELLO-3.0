#!/bin/bash

# this automated setup only works on Github Codespaces

# check if brew is installed, and install if necessary
if ! command -v brew & > /dev/null
then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/codespace/.profile
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
fi

# install redis using brew
brew install redis

# install required Python packages
pip install redis dash dash-core-components dash-html-components requests
