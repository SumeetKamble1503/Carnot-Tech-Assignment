#!/bin/bash

# set -e
cmd="$@"
echo $cmd

echo "Env: $ENVIRONMENT"


if [ -f .env ]; then
    source .env
    echo "Environment variables loaded from .env file"
else
    echo ".env file not found"
fi


if [[ $ENVIRONMENT == "dev" ]]; then
    python3 app.py
else
    # code to run on other environments
    # uwsgi --ini uwsgi.ini
fi

