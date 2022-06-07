FROM python:3

RUN apt-get clean && \
    apt-get -y update && \
    apt-get install -y --no-install-recommends \
    unzip bzip2 \
    curl wget \
	vim \
    git \
    mecab mecab-ipadic libmecab-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY requirements.txt /work

RUN pip install --no-cache-dir -r requirements.txt
RUN cp /etc/mecabrc /usr/local/etc/

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs
ENV PYTHONIOENCODING utf-8
