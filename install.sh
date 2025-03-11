INSTALL_DIR="/usr/local/lib/MieleRESTServer/"

#!/bin/bash
systemctl stop MieleRESTServer
mkdir -p "$INSTALL_DIR"
cp *.py "$INSTALL_DIR"
cp -r templates/ "$INSTALL_DIR"
cp *.service /etc/systemd/system/
useradd --system mieleserver
sudo -u mieleserver pip install -r ./requirements.txt
systemctl daemon-reload
systemctl restart MieleRESTServer
