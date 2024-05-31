ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    proj-bin

WORKDIR /app
COPY ./requirements.txt .

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
    
COPY ./ .

RUN chmod u+x tests.sh

CMD ./tests.sh