#!/bin/sh
read -p "Please enter an e-mail adress for your new user: " user

docker exec -it dovecot doveadm pw -s BLF-CRYPT

read -p "Please copy the hash above, excluding {BLF-CRYPT}: " hash

echo "Please enter mysql root password next."
docker exec -it database mysql -u root -p mailserver -e "INSERT INTO virtual_users (domain_id, password , email) VALUES ('1', '$hash', '$user');"
