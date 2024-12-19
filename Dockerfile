FROM python:3.12.4-slim-bookworm
WORKDIR /app
RUN cp /app/debian.sources /etc/apt/sources.list.d \
    && apt-get update && apt install portaudio19-dev -y \
    && pip install aiohttp pyaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT  ["python", "/app/main.py"]