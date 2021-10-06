#!/bin/bash

name="dwayne.sh"

echo "$name : Running Dwayne script..."
if test -f "main.py"; then
    echo "$name : Do not execute dwayne.sh in the same directory as Dwayne (otherwise duplicate files will be created)."
    exit 1
fi
if ! test -f "token.txt"; then
    echo "$name : Token not found; paste your bot's token here: "
    read token
    echo "$token" > token.txt
fi
echo "$name : Deleting old Dwayne files..."
rm -frv dwayne
echo "$name : Cloning new Dwayne files from Github repo..."
git clone https://github.com/marceloclubhouse/dwayne
cd dwayne || return
if [ ! -d "venv" ]; then
    echo "$name : Virtual environment not found."
    echo "$name : Installing virtualenv..."
    pip3 install virtualenv
    echo "$name : Creating virtual environment..."
    virtualenv venv
    source venv/bin/activate
    echo "$name : Installing Dwayne's packages..."
    pip3 install -r "requirements.txt"
    echo "$name : Exiting environment and going back to root directory..."
    deactivate
    cd ..
fi
source dwayne/venv/bin/activate
echo "$name : Running Dwayne"
python3 dwayne/main.py "$(cat token.txt)"