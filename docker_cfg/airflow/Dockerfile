# our base image
FROM apache/airflow:1.10.12-python3.7

# copying necessary files from local into the image
COPY ./airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY ./requirements.txt /opt/requirements.txt
COPY ./entrypoint /entrypoint

USER root

RUN sudo apt-get update -y -q  \
    && sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade  -y -q \
    && apt-get install -y  --no-install-recommends \
                vim \
                && chown -R airflow: /opt \
                && chmod a+x /entrypoint \
                && apt-get clean \
                && rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /opt/

RUN $(command -v pip) install --user --no-cache-dir -r /opt/requirements.txt
