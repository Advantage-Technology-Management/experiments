#!/usr/bin/env bash

USER_NAME=admin
INSTANCE_URL=http://localhost
PASSWORD="S%j7?v<H{S3nTWgD[zjV0c*y"


while IFS="" read -r p || [ -n "$p" ]
do
echo "curl -s -u $USER_NAME:\"$PASSWORD\" -X POST -F path=\"${p}\" -F cmd=\"activate\" https://author-loblaw-stage.adobecqms.net/bin/replicate.json"
curl -u $USER_NAME:"$PASSWORD" -X POST -F path="${p}" -F cmd="activate" https://author-loblaw-stage.adobecqms.net/bin/replicate.json 
done < fixURL.csv
