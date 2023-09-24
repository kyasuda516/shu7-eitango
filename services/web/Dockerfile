FROM nginx:stable-alpine AS builder
# GetoIP2's latest version can be known at https://github.com/leev/ngx_http_geoip2_module/tags
ARG NGX_HTTP_GEOIP2_MODULE_VERSION=3.4
RUN NGINX_VERSION=`nginx -v 2>&1 | cut -d '/' -f 2` \
 && cd /tmp/ \
 && wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O nginx-${NGINX_VERSION}.tar.gz \
 && wget https://github.com/leev/ngx_http_geoip2_module/archive/${NGX_HTTP_GEOIP2_MODULE_VERSION}.tar.gz -O ngx_http_geoip2_module-${NGX_HTTP_GEOIP2_MODULE_VERSION}.tar.gz \
 && apk add --no-cache --virtual dependency gcc libc-dev make openssl-dev pcre-dev zlib-dev linux-headers \
 && apk add --update-cache libmaxminddb-dev logrotate \
 && tar zxf nginx-${NGINX_VERSION}.tar.gz \
 && tar zxf ngx_http_geoip2_module-${NGX_HTTP_GEOIP2_MODULE_VERSION}.tar.gz \
 && cd ./nginx-${NGINX_VERSION}/ \
 && CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^configure arguments: //p') \
 && ./configure --with-compat --add-dynamic-module=../ngx_http_geoip2_module-${NGX_HTTP_GEOIP2_MODULE_VERSION} \
 && make modules \
 && apk del dependency

FROM nginx:stable-alpine-slim AS base
ENV TZ="Asia/Tokyo"
RUN unlink /var/log/nginx/access.log \
 && unlink /var/log/nginx/error.log
COPY --from=builder /var/cache/apk/* /var/cache/apk/
RUN apk add libmaxminddb-dev logrotate \
 && rm -rf /var/cache/apk/* \
 && rm /etc/logrotate.conf
COPY --from=builder /tmp/nginx-${NGINX_VERSION}/objs/ngx_http_geoip2_module.so /etc/nginx/modules/
COPY ./nginx.logrotate /
EXPOSE 443

FROM base AS dev

FROM base AS base2
RUN chmod gu+s /usr/sbin/nginx /usr/sbin/logrotate
COPY ./nginx.conf /etc/nginx/
USER nginx

FROM base2 AS stg
COPY ./default.stg.conf /etc/nginx/conf.d/default.conf

FROM base2 AS prod
# COPY ./default.first.prod.conf /etc/nginx/conf.d/default.conf
COPY ./default.prod.conf /etc/nginx/conf.d/default.conf