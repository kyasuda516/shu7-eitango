FROM grafana/grafana:10.1.0 AS base
ENV GF_EXPLORE_ENABLED true
EXPOSE 3128

FROM base AS dev

FROM base AS stg
COPY --chmod=644 ./grafana.ini /etc/grafana/

FROM stg AS prod