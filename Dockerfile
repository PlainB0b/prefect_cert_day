FROM prefecthq/prefect:2.10.15-python3.7
COPY . /opt/prefect/prefect_cert_day/
WORKDIR /opt/prefect/prefect_cert_day/
