FROM grafana/promtail:2.8.4 AS base
ENV TZ="Asia/Tokyo"
CMD ["-config.file=/etc/promtail/myconfig.yaml"]

FROM base AS dev
EXPOSE 9080

FROM base AS stg
COPY --chmod=644 ./config.yaml /etc/promtail/myconfig.yaml
RUN useradd -M promtail
USER promtail

FROM stg AS prod