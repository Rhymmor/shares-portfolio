#!/bin/bash

cd notebooks

for f in *.ipynb; do
    poetry run jupyter nbconvert --execute --to notebook --inplace $f &
done;

wait
