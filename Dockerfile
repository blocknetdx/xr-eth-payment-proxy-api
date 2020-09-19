FROM python:3.7-alpine3.9

COPY . /app/manager
WORKDIR /app/manager

RUN apk update && apk add libpq
RUN apk add --no-cache build-base musl-dev gcc g++ openssl-dev libffi-dev python-dev postgresql-dev \
    && pip install cython \
    && pip install psycopg2-binary \
    && pip3 install -r /app/manager/requirements.txt \
    && apk del build-base musl-dev gcc g++ openssl-dev \
    && rm -rf /var/cache/apk/* \
    && rm -rf /usr/share/man \
    && rm -rf /tmp/*

CMD ["python3", "/app/manager/main.py"]
