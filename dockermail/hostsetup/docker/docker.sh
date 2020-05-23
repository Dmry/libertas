#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root."
  exit
fi

apt install -y docker python3-pip 
pip3 install pip-upgrade-outdated docker-compose