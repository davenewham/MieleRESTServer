#!/bin/bash

INSTALL_DIR="/usr/local/lib/MieleRESTServer"
SERVICE_NAME="MieleRESTServer"
LOCAL_ACCOUNT="mieleserver"
VENV_NAME="venv_"$SERVICE_NAME
systemctl stop $SERVICE_NAME
mkdir -p "$INSTALL_DIR"
cp *.py "$INSTALL_DIR"
cp -r templates/ "$INSTALL_DIR"
cp *.service /etc/systemd/system/
python -m venv $VENV_NAME
"$VENV_NAME"/bin/pip install -r ./requirements.txt
cp -r $VENV_NAME "$INSTALL_DIR"/$VENV_NAME
useradd --system "$LOCAL_ACCOUNT"
#sudo -u "$LOCAL_ACCOUNT" pip install -r ./requirements.txt
systemctl daemon-reload
systemctl restart $SERVICE_NAME
