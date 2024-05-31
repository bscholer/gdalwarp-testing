#!/bin/bash

echo "GDAL version"
gdalinfo --version
echo "PROJ version"
proj

gdalinfo /data/bardstown_itrf.tif

python3 main.py