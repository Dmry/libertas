#!/bin/sh

if [ "$EUID" -ne 0 ]
  then echo "Please run as root."
  exit
fi

apt install -y fail2ban

containers=(dovecot postfix)

for item in ${array[*]}
do
    cp fail2ban-$item-action.conf /etc/fail2ban/action.d/
    cp fail2ban-$item-filter.conf /etc/fail2ban/filter.d/
done

cp jail.local /etc/fail2ban/

echo "ssh port?"

read ssh

sed -i 's/port = ssh/port = $ssh/g' /etc/fail2ban/jail.local