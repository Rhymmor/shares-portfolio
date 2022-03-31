#!/bin/bash

for f in notebooks/*.ipynb; do
    poetry run jupyter nbconvert ${f} --to html --output-dir docs/pages &
done;

wait
