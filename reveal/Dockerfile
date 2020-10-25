FROM        alpine

RUN         addgroup -S reveal && adduser -S -h /var/lib/reveal-multiplex -s /sbin/nologin -DH -G reveal reveal

RUN         apk --update add nodejs-npm setpriv

RUN         cd reveal.js; npm install

CMD         /ext/init