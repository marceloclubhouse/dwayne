#!/bin/bash

# dwayne
# A back-end Discord bot created as an alternative to Groovy and Rhythm
# Copyright (C) 2021 Marcelo Cubillos
# This project is available under the MIT license, see LICENSE.txt for more details
#
# dwayne.sh

RED='\033[0;31m'
NC='\033[0m'
name="${RED}dwayne.sh${NC}"

echo -e "$name : Running Dwayne script..."
if test -f "main.py"; then
    echo -e "$name : Do not execute dwayne.sh in the same directory as Dwayne (otherwise duplicate files will be created)."
    exit 1
fi
if ! test -f "token.txt"; then
    echo -e "$name : Token not found; paste your bot's token here: "
    read token
    echo -e "$token" > token.txt
fi
if ! test -f "yt_api_key.txt"; then
    echo -e "$name : YouTube Data API key not found. If you want to enable play queries (e.g. '!play here comes the sun'), paste an API key here: "
    read yt_key
    if [ -n "$yt_key" ]; then
        echo -e "$name : Saving token as dwayne/yt_api_key.txt"
        echo "$yt_key" > yt_api_key.txt
    fi
fi
echo -e "$name : Deleting old Dwayne files..."
rm -frv dwayne
echo -e "$name : Cloning new Dwayne files from Github repo..."
git clone https://github.com/marceloclubhouse/dwayne
git checkout multiserver
cd dwayne || return
if [ ! -d "venv" ]; then
    echo -e "$name : Virtual environment not found."
    echo -e "$name : Installing virtualenv..."
    pip3 install virtualenv
    echo -e "$name : Creating virtual environment..."
    python3 -m virtualenv venv
    source venv/bin/activate
    echo -e "$name : Installing Dwayne's packages..."
    pip3 install -r "requirements.txt"
    echo -e "$name : Copying YouTube Data API Key to dwayne/yt_api_key.txt"
    cp ../yt_api_key.txt yt_api_key.txt
    echo -e "$name : Exiting environment and going back to root directory..."
    deactivate
    cd ..
fi
source dwayne/venv/bin/activate
echo -e "$name : Running Dwayne"
python3 dwayne/main.py "$(cat token.txt)"