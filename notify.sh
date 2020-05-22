#!/usr/bin/env bash

# export API_KEY="<LONG_API_KEY_HERE>"
# export HOST="http://localhost:5000"
TOPIC_CODE="$1"
MESSAGE="$2"
API_URL="${HOST%/}/api/notify"

if [ -z "$API_KEY" ]; then echo "API_KEY environment variable not defined" && exit 1; fi
if [ -z "$HOST" ]; then echo "HOST environment variable not defined" && exit 1; fi
if [ -z "$TOPIC_CODE" ]; then echo "TOPIC_CODE (first argument) not defined" && exit 1; fi
if [ -z "$MESSAGE" ]; then echo "MESSAGE (second argument) not defined" && exit 1; fi

echo "Sending to API '$API_URL' topic '$TOPIC_CODE' message '$MESSAGE'"
curl -G "$API_URL" \
    --data-urlencode "api_key=$API_KEY" \
    --data-urlencode "topic_code=$TOPIC_CODE" \
    --data-urlencode "message=$MESSAGE"
