FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

RUN apt-get update && apt-get install -y \
    python3-pip \
    proj-bin

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./ .

RUN chmod u+x tests.sh

CMD ./tests.sh