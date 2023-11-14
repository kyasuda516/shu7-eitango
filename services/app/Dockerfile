ARG PYTHON_VERSION=3.11.5
# [NB] If you change the minor version number (Y of X.Y.Z), also change the directory number in the dev and stg stages.

FROM python:${PYTHON_VERSION} AS export
RUN pip --no-cache-dir install pipenv
COPY --chmod=644 ./Pipfile ./
RUN sed -i s/%pythonVersion%/${PYTHON_VERSION}/g ./Pipfile \
 && pipenv lock \
 && pipenv requirements > /requirements.lock \
 && pipenv requirements --dev > /requirements-dev.lock

FROM python:${PYTHON_VERSION} AS builder
COPY --from=export /requirements.lock /
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /requirements.lock

FROM python:${PYTHON_VERSION} AS dev-builder
COPY --from=export /requirements-dev.lock /
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /requirements-dev.lock

FROM python:${PYTHON_VERSION}-slim AS base
ENV TZ="Asia/Tokyo"
WORKDIR /app/
RUN apt update \
 && apt -y upgrade \
 && apt -y install libpq5 libxml2 \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
EXPOSE 3031

FROM base AS dev
COPY --from=dev-builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=dev-builder /usr/local/bin/ /usr/local/bin/

FROM base AS stg
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
RUN useradd -M uwsgi \
 && chmod gu+s /usr/local/bin/uwsgi /usr/local/bin/python
COPY --chmod=644 ./ ./
RUN rm ./Pipfile
USER uwsgi

FROM stg AS prod