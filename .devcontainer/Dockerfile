# Dockerfile to create container with Cell Ranger v9.0.0
# Push to ccrsfifx/cellranger:9.0.0

FROM docker.io/manimcommunity/manim:v0.19.0
LABEL authors="Shaoun Xie <xieshaojun0526@gmail.com>" \
    description="Docker image for manim"

USER root
RUN echo "root:manimuser" | chpasswd
# Install dependencies and SoX
RUN apt-get update --quiet && \
    apt-get install sox --yes && \
    apt-get install -y build-essential libtool libasound2-dev portaudio19-dev python3-pyaudio && \
    apt-get install -y xdg-utils && \
    apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Verify installation
RUN sox --version

RUN pip3 install --no-cache-dir \
    pandas==2.2.3 \
    matplotlib==3.4.3 \
    pytest==8.3.5 \
    pytest-cov==4.0.0 \
    twine==6.1.0

USER manimuser

## docker build -t manim -f Dockerfile .
##  docker run -v "${PWD}:${PWD}" -w "${PWD}" -it -p 8888:8888 manim:latest jupyterlab --ip=0.0.0.0