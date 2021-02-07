FROM python:3
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /linkgraph/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /linkgraph/requirements.txt

WORKDIR /linkgraph

ADD . .