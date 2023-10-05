#!/bin/bash

# Generate values
UUID=$(uuidgen)
output=$(docker exec 3x-ui sh -c "/app/bin/xray-linux-amd64 x25519")

PRIVATE_KEY=$(echo "$output" | awk -F': ' '/Private key/ {print $2}')
PUBLIC_KEY=$(echo "$output" | awk -F': ' '/Public key/ {print $2}')

echo "Private key: $PRIVATE_KEY"
echo "Public key: $PUBLIC_KEY"

# Create inbounds.sql
cat > inbounds.sql << EOF
BEGIN TRANSACTION;
DROP TABLE IF EXISTS "inbounds";
CREATE TABLE IF NOT EXISTS "inbounds" (
    "id"    integer,
    "user_id"   integer,
    "up"    integer,
    "down"  integer,
    "total" integer,
    "remark"    text,
    "enable"    numeric,
    "expiry_time"   integer,
    "listen"    text,
    "port"  integer UNIQUE,
    "protocol"  text,
    "settings"  text,
    "stream_settings" text,
    "tag"   text UNIQUE,
    "sniffing"  text,
    PRIMARY KEY("id")
);
INSERT INTO "inbounds" VALUES (1,1,0,0,0,'',1,0,'',443,'vless','{
  "clients": [
    {
      "id": "$UUID",
      "flow": "xtls-rprx-vision",
      "email": "default418",
      "limitIp": 0,
      "totalGB": 0,
      "expiryTime": 0,
      "enable": true,
      "tgId": "",
      "subId": ""
    }
  ],
  "decryption": "none",
  "fallbacks": []
}','{
  "network": "tcp",
  "security": "reality",
  "realitySettings": {
    "show": false,
    "xver": 0,
    "dest": "dl.google.com:443",
    "serverNames": [
      "dl.google.com"
    ],
    "privateKey": "$PRIVATE_KEY",
    "minClient": "",
    "maxClient": "",
    "maxTimediff": 0,
    "shortIds": [
      "deced1f3"
    ],
    "settings": {
      "publicKey": "$PUBLIC_KEY",
      "fingerprint": "chrome",
      "serverName": "",
      "spiderX": "/"
    }
  },
  "tcpSettings": {
    "acceptProxyProtocol": false,
    "header": {
      "type": "none"
    }
  }
}','inbound-443','{
  "enabled": true,
  "destOverride": [
    "http",
    "tls",
    "quic",
    "fakedns"
  ]
}');
COMMIT;
EOF

