FROM python:3.12.4-slim-bookworm
WORKDIR /app
COPY heartale/ /app/
RUN mv /app/debian.sources /etc/apt/sources.list.d/ &&\
    apt-get update &&\
    apt-get install -y --no-install-recommends git wget &&\
    python -m pip install --upgrade pip &&\
    pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


