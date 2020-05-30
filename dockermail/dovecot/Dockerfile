FROM alpine:latest

RUN addgroup -g 3001 dovecot
RUN addgroup -g 3003 postfix
RUN adduser -D -s /sbin/nologin -u 2001 -G dovecot dovecot
RUN adduser -D -s /sbin/nologin -u 1000 -G postfix postfix

RUN apk add -uU openssl ca-certificates dovecot dovecot-lmtpd dovecot-mysql && \
    rm -rf /var/cache/apk/* &&\
    echo "0       4       *       *       *       apk update && apk upgrade > /var/log/cron-apk.log" >> /var/spool/cron/crontabs/root

ADD dovecot.conf /etc/dovecot/dovecot.conf
ADD dovecot-sql.conf.ext /etc/dovecot/dovecot-sql.conf.ext
ADD conf.d/ /etc/dovecot/conf.d/

RUN chown -R mail:dovecot /etc/dovecot &&\
    chmod -R o-rwx /etc/dovecot

RUN mkdir -p /var/spool/postfix/private/dovecot

RUN install -d -o mail -g dovecot /mail

ENTRYPOINT ["dovecot"]
CMD ["-F"]
