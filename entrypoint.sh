#!/usr/bin/env bash

# When any line or pipe fails, fail altogether 
set -eu

# Regardless of parameters, wait for database
echo "[Entrypoint]: Waiting until database is up?"
./wait

# Custom parameters provided
if [ ! $# -eq 0 ]
then
    echo "[Entrypoint]: Running non-default command - '$*'"
    bash -c "$*"
    exit $?
fi

# No parameters provided
echo "[Entrypoint]: Upgrading database"
flask db upgrade

echo "[Entrypoint]: Running server"
flask run --host "$X12_HOST" --port "$X12_PORT"
