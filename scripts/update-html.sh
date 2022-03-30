#!/bin/bash
set -xe

jupyter nbconvert *.ipynb --to html --output-dir docs/pages
git add docs/pages/*.html