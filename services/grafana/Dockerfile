FROM grafana/grafana:10.1.0 AS base
ENV GF_EXPLORE_ENABLED true
EXPOSE 3128

FROM base AS dev

FROM base AS stg
COPY --chmod=644 ./grafana.ini /etc/grafana/
COPY --chmod=644 ./provisioning/datasources.yaml /etc/grafana/provisioning/datasources/
COPY --chmod=644 ./provisioning/dashboards.yaml  /etc/grafana/provisioning/dashboards/
COPY --chmod=644 ./provisioning/dashboard1.json  /var/lib/grafana/dashboards/
COPY --chmod=644 ./provisioning/alerting.yaml    /etc/grafana/provisioning/alerting/

FROM stg AS prod