#!/bin/bash
MIELEIP="$1"
echo "Trying HTTP"
wget --tries=2 --timeout=3 --connect-timeout=3 -O - --method=PUT --body-file="$2" http://$MIELEIP/Security/Commissioning
echo "Trying HTTPS"
wget --tries 2 --timeout=3 --no-check-certificate -O - --method=PUT --body-file="$2" https://$MIELEIP/Security/Commissioning
