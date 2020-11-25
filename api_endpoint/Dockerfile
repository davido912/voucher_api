FROM python:3.7-slim-buster

COPY requirements.txt /requirements.txt
COPY ./pg_connect.py /api_endpoint/pg_connect.py
COPY ./endpoints_rendering.py /api_endpoint/voucher_segments.py
COPY ./voucher_selection_api.py /api_endpoint/voucher_selection_api.py
ADD ./templates /api_endpoint/templates

RUN apt-get update -y -q  \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade  -y -q \
    && apt-get install -y  --no-install-recommends \
                vim \
                build-essential \
                gnupg2 \
                libpq-dev \
                && apt-get clean \
                && rm -rf /var/lib/apt/lists/*

RUN $(command -v pip) install --user --no-cache-dir -r /requirements.txt