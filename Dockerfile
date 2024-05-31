FROM osgeo/gdal:ubuntu-full-3.6.3

RUN gdal --version
RUN proj --version

RUN apt-get update && apt-get install -y \
    python3-pip
