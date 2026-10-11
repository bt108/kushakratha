#!/bin/sh

first=1

for file in "$@"; do
  if [ "$first" -eq 0 ]; then
    printf '<++>\n'
  fi
  cat -- "$file"
  first=0
done
