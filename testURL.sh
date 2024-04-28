#!/usr/bin/env bash


while IFS="" read -r p || [ -n "$p" ]
do
echo "${p}"
curl  --silent --output /dev/null --show-error --fail ${p}
#done < testurl.csv
done < StageURLSNew650.csv
