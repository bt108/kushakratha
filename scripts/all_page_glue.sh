#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p log

for book in $(printf "%s\n" *_page*.txt | sed 's/_page.*//' | sort -u); do
  ls "${book}"_page*.txt | sort -V  | xargs "$SCRIPT_DIR/page_glue.sh" | $SCRIPT_DIR/autofix-comb.py | $SCRIPT_DIR/autofix-empty.py | $SCRIPT_DIR/autofix-ws.py | $SCRIPT_DIR/autofix-nfc.py | $SCRIPT_DIR/find_artifacts.py > "${book}.md" 2> ./log/${book}.log
done

find ./log/ -type f -empty -delete
