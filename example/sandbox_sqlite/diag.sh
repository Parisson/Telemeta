#!/bin/sh

app="telemeta"
dir="../../doc/devel"

python modelviz.py -a > $dir/$app-all.dot
python modelviz.py $app > $dir/$app.dot

dot $dir/$app-all.dot -Tpdf -o $dir/$app-all.pdf
dot $dir/$app.dot -Tpdf -o $dir/$app.pdf

