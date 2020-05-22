#!/usr/bin/env bash

TOPIC_CODE=$1
MESSAGE=$2
API_URL="http://localhost:5000/api/notify"

if [ -z $API_KEY ]; then echo "API_KEY environment variable not defined" && exit 1; fi
if [ -z $TOPIC_CODE ]; then echo "TOPIC_CODE (first argument) not defined" && exit 1; fi
if [ -z $MESSAGE ]; then echo "MESSAGE (second argument) not defined" && exit 1; fi

echo "Sending to topic '$TOPIC_CODE' message '$MESSAGE'"
curl -X GET "$API_URL?api_key=$API_KEY&topic_code=$TOPIC_CODE&message=$MESSAGE"