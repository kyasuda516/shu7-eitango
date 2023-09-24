FROM grafana/loki:2.8.4 AS base
CMD ["-config.file=/etc/loki/myconfig.yaml"]

FROM base AS dev

FROM base AS stg
COPY --chmod=644 ./config.yaml /etc/loki/myconfig.yaml

FROM stg AS prod