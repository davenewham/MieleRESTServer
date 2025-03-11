INSTALL_DIR="/usr/local/lib/MieleRESTServer/"
SERVICE_NAME="MieleRESTServer"
LOCAL_ACCOUNT="mieleserver"
#!/bin/bash
systemctl stop $SERVICE_NAME
mkdir -p "$INSTALL_DIR"
cp *.py "$INSTALL_DIR"
cp -r templates/ "$INSTALL_DIR"
cp *.service /etc/systemd/system/
useradd --system "$LOCAL_ACCOUNT"
sudo -u "$LOCAL_ACCOUNT" pip install -r ./requirements.txt
systemctl daemon-reload
systemctl restart $SERVICE_NAME
