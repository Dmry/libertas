#!/bin/bash

cd /ext/reveal.js

exec setpriv --reuid=reveal --regid=reveal --init-groups --reset-env npm start