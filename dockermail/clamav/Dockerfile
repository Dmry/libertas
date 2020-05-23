FROM alpine:latest

LABEL maintainer="Daniël Emmery : github.com/dmry"

RUN apk add -uU clamav clamav-milter freshclam supervisor && \
    rm -rf /var/cache/apk/* &&\
    echo "0       4       *       *       *       apk update && apk upgrade > /var/log/cron-apk.log" >> /var/spool/cron/crontabs/root

COPY ./clamav-milter.conf /etc/clamav/
COPY ./clamd.conf /etc/clamav/

RUN install -d -o clamav -g clamav /var/run/clamav

COPY ./supervisord.d/*.ini /etc/supervisord.d/
COPY ./supervisord.conf /etc/

RUN freshclam

ENTRYPOINT ["supervisord"]
CMD []
