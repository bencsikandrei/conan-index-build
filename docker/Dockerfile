FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y apt-transport-https \
    ca-certificates \
    gnupg \
    software-properties-common \
    wget \
    git \
    python \
    python3-pip \
    g++

WORKDIR /workspace/conan

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN conan profile new default --detect && \
    conan profile update settings.compiler.libcxx=libstdc++11 default
