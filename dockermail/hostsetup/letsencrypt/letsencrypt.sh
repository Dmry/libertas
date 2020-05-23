#!/bin/bash

echo "This will install letsencrypt, generate a certificate for you domain and set cron to autorenew."
echo "WARNING: If you already have a certificate, please edit docker-compose.yml to mount the correct certificate in the postfix and dovecot containers."
read -p "If you already have a certificate, do NOT choose yes. Contine (y/n)?" answer

if [ "$EUID" -ne 0 ]
  then echo "Please run as root."
  exit
fi

while true
do
  case $answer in
   [yY]* )  echo "Domain name?"

            read domain

            apt install -y letsencrypt
            certbot certonly -d $domain

            echo "0 4 1 * * letsencrypt renew" > /var/spool/cron/crontabs/root

            break;;
   [nN]* )  exit;;

   * )      echo "y or n."; break ;;
  esac
done