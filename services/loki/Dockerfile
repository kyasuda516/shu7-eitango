FROM grafana/loki:2.9.2 AS base
CMD ["-config.file=/etc/loki/myconfig.yaml"]

FROM base AS dev

FROM base AS stg
COPY --chmod=644 ./config.yaml /etc/loki/myconfig.yaml

FROM stg AS prod