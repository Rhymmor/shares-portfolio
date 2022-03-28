#!/bin/bash
set -xe

jupyter nbconvert *.ipynb --to html --output-dir pages
git add pages/*.html