FROM mysql:8.0.35 AS base
ENV TZ="Asia/Tokyo" LANG=ja_JP.UTF-8 LC_ALL=ja_JP.UTF-8 LANGUAGE=ja_JP:ja
RUN microdnf install -y glibc-locale-source \
 && localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
COPY --chmod=644 ./my.cnf /etc/mysql/conf.d/

FROM base AS dev

FROM base AS stg
COPY --chown=mysql:mysql ./initialize.sh /docker-entrypoint-initdb.d/
COPY --chown=mysql:mysql ./mysql-files/ /var/lib/mysql-files/
USER mysql

FROM stg AS prod