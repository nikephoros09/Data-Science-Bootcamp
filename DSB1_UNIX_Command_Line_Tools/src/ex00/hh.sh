#!/bin/sh

JOB_NAME=$(echo "$1" | tr ' ' '+')
URL="https://api.hh.ru/vacancies?text=${JOB_NAME}&per_page=20"

curl -s -H "User-Agent: api-test-agent" "$URL" | jq . > hh.json
