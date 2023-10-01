#!/bin/bash
echo -e "
          _  _   _  ___
         | || | / |( _ )
         | || |_| |/ _ \
         |__   _| | (_) |
            |_| |_|\___/ "
echo -e "Welcome to 3X-UI Docker + Traefik + TelegramBot installation script"

read -p "Enter username for 3X-UI Panel: " usernameTemp
read -p "Enter password: " passwordTemp
read -p "Enter port on which 3X-UI would be available: " config_port
read -p "Enter your hostname:" hostname_input
read -p "Enter your e-mail for certificate:" email_input
read -p "Enter your Telegram bot API token:" tgtoken_input

export USERNAME=$usernameTemp
export PASSWORD=$passwordTemp
export CONFIG_PORT=$config_port
export HOSTNAME=$hostname_input
export EMAIL=$email_input
export TGTOKEN=$tgtoken_input

docker compose up -d
docker exec 3x-ui sh -c "/app/x-ui setting -username $usernameTemp -password $passwordTemp"
sleep 1
docker restart 3x-ui
echo -e "3X-UI + Traefik + TelegramBot installation finished, admin panel is available on https://"$hostname_input":"$config_port