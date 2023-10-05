#!/bin/bash

function check_uuidgen() {
    if ! command -v uuidgen &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y uuid-runtime
    fi
}

function check_docker() {
    packages=(docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin)
    for pkg in "${packages[@]}"; do
        if ! dpkg-query -l | grep -qw "$pkg"; then
            return 1
        fi
    done
    return 0
}

function install_docker() {
    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    if [[ $(lsb_release -is) == "Debian" ]]; then
        curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
          $(lsb_release -cs) stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    elif [[ $(lsb_release -is) == "Ubuntu" ]]; then
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    else
        echo "Unsupported OS"
        exit 1
    fi
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    sudo apt-get update
    sudo apt-get install "${packages[@]}"
}

function clone_repo() {
    if [[ ! -d "team_418" ]]; then
        git clone https://github.com/torikki-tou/team_418.git
    fi
    cd team_418 || exit
}

check_uuidgen
check_docker
if [[ $? -ne 0 ]]; then
    read -p "Docker components are missing, would you like to install them? (y/n): " response
    if [[ $response == "y" ]]; then
        install_docker
    else
        echo "Aborting"
        exit 1
    fi
fi

clone_repo

echo -e "
          _  _   _  ___
         | || | / |( _ )
         | || |_| |/ _ \
         |__   _| | (_) |
            |_| |_|\___/ "
echo -e "Welcome to 3X-UI Docker + Traefik + TelegramBot installation script"

read -p "Enter username for 3X-UI Panel: " usernameTemp
read -p "Enter password: " passwordTemp
read -p "Enter port on which 3X-UI web admin panel would be available: " config_port
read -p "Enter your hostname (WWW or Domain):" hostname_input
read -p "Enter your e-mail for certificate :" email_input
read -p "Enter your Telegram bot API token (use Tg BotFather):" tgtoken_input
read -p "Enter your Telegram admin profile (as @admin without @):" tgadminid_input

export USERNAME=$usernameTemp
export PASSWORD=$passwordTemp
export CONFIG_PORT=$config_port
export HOSTNAME=$hostname_input
export EMAIL=$email_input
export TGTOKEN=$tgtoken_input
export ADMINID=$tgadminid_input

docker compose up -d
docker exec 3x-ui sh -c "/app/x-ui setting -username $usernameTemp -password $passwordTemp"
sleep 1
docker restart 3x-ui
sleep 3
./inbounds_gen.sh
docker restart 3x-ui
echo -e "3X-UI + Traefik + TelegramBot installation finished, XTLS-Reality default config added, admin panel is available on https://"$hostname_input":"$config_port
