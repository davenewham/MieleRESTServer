#!/bin/bash
systemctl stop MieleRESTServer
mkdir -p /usr/local/lib/MieleRESTServer/
cp *.py /usr/local/lib/MieleRESTServer/
cp -r templates/ /usr/local/lib/MieleRESTServer/
cp *.service /etc/systemd/system/
useradd --system mieleserver
sudo -u mieleserver pip install -r ./requirements.txt
systemctl daemon-reload
systemctl restart MieleRESTServer
