#!/bin/bash

function check_sqlite3() {
    if ! command -v sqlite3 &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y sqlite3
    fi
}

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
    sudo apt-get install -y ca-certificates curl gnupg
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
    sudo apt-get install -y "${packages[@]}"
}
function check_unzip() {
    if ! command -v unzip &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y unzip
    fi
}

function check_inbounds_table() {
    current_dir=$(pwd)
    db_path="$current_dir/db/x-ui.db"
    if [[ -f "$db_path" ]]; then
        table_exists=$(sqlite3 "$db_path" "SELECT name FROM sqlite_master WHERE type='table' AND name='inbounds';")
        if [[ $table_exists == "inbounds" ]]; then
            read -p "The 'inbounds' table already exists. Do you want to proceed with the execution of inbounds_gen.sh? (y/n): " response
            if [[ $response == "y" ]]; then
                ./inbounds_gen.sh
		sqlite3 $db_path < inbounds.sql
		echo -e "Added XTLS-Reality config entry into x-ui.db database"
            else
                echo "Skipping execution of inbounds_gen.sh."
            fi
        else
            ./inbounds_gen.sh
	    sqlite3 $db_path < inbounds.sql
        fi
    else
        echo "x-ui.db does not exist in $db_path. Proceeding with the rest of the setup."
    fi
}

function clone_repo() {
    if [[ -d "team_418" ]]; then
        cd team_418 || exit
        # Here you might want to fetch and unzip again or just rely on the existing content.
        # We're assuming that you want to fetch the newest content. 
        # So we'll remove the old files, fetch the new .zip and then unzip.
        rm -rf *
        wget https://github.com/torikki-tou/team418/archive/refs/heads/testing.zip
        unzip testing.zip
        mv team418-testing/* .
        rm -rf team418-testing testing.zip
    else
        wget https://github.com/torikki-tou/team418/archive/refs/heads/testing.zip
        unzip testing.zip
        mkdir -p team_418
        mv team418-testing/* team_418/
        cd team_418 || exit
        rm -rf ../team418-testing ../testing.zip
    fi
}


check_uuidgen
check_sqlite3
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

check_unzip
clone_repo
chmod +x inbounds_gen.sh
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

export XUI_USERNAME=$usernameTemp
export XUI_PASSWORD=$passwordTemp
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

check_inbounds_table

docker restart 3x-ui
echo -e "3X-UI + Traefik + TelegramBot installation finished, XTLS-Reality default config added, admin panel is available on https://"$hostname_input":"$config_port
