FROM python:3.12.4-slim-bookworm

WORKDIR /app

COPY . /app/

RUN mv /app/deploy/debian.sources /etc/apt/sources.list.d/debian.sources \
    && apt update -y && apt upgrade -y \
    && apt install -y --no-install-recommends \
        tar curl bzip2 \
    && pip install flask pyyaml numpy soundfile sherpa-onnx requests\
        -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

ENTRYPOINT ["python", "app.py"]