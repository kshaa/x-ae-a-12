#!/usr/bin/env bash

export API_KEY="<API_KEY>"
export HOST="http://localhost:5000/"
export TOPIC_CODE="test"

./notify.sh "$TOPIC_CODE" "$1"