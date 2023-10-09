#!/bin/bash

#Check if script executed by root
function isRoot() {
	if [ "$EUID" -ne 0 ]; then
		return 1
	fi
}

#Check if sqlite3 package is installed
function check_sqlite3() {
    if ! command -v sqlite3 &> /dev/null; then
        apt-get update
        apt-get install -y sqlite3
    fi
}

#Check if uuid-runtime package is installed
function check_uuidgen() {
    if ! command -v uuidgen &> /dev/null; then
        apt-get update
        apt-get install -y uuid-runtime
    fi
}
#Check if the docker-ce packages are installed
function check_docker() {
    packages=(docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin)
    for pkg in "${packages[@]}"; do
        if ! dpkg-query -l | grep -qw "$pkg"; then
            return 1
        fi
    done
    return 0
}

#Install docker packages from docker.com repo
function install_docker() {
    apt-get update
    apt-get install -y ca-certificates curl gnupg
    install -m 0755 -d /etc/apt/keyrings
    if [[ $(lsb_release -is) == "Debian" ]]; then
        curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
          $(lsb_release -cs) stable" | \
          tee /etc/apt/sources.list.d/docker.list > /dev/null
    elif [[ $(lsb_release -is) == "Ubuntu" ]]; then
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | \
          tee /etc/apt/sources.list.d/docker.list > /dev/null
    else
        echo "Unsupported OS"
        exit 1
    fi
    chmod a+r /etc/apt/keyrings/docker.gpg
    apt-get update
    apt-get install -y "${packages[@]}"
	echo -e "\e[34mDocker packages were installed\e[0m"
}

#Check for unzip package installed
function check_unzip() {
    if ! command -v unzip &> /dev/null; then
        apt-get update
        apt-get install -y unzip
    fi
}

#Checks if "inbounds" table exists in x-ui.db, and if the inbound_gen script can be executed
function check_inbounds_table() {
    current_dir=$(pwd)
    db_path="$current_dir/db/x-ui.db"
    if [[ -f "$db_path" ]]; then
        table_exists=$(sqlite3 "$db_path" "SELECT name FROM sqlite_master WHERE type='table' AND name='inbounds';")
        if [[ $table_exists == "inbounds" ]]; then
            read -p "The 'inbounds' table already exists. On first run it's empty, you can safely continue. Do you want to overwrite existing 3X-UI config? (y/n): " response
            if [[ $response == "y" ]]; then
                ./inbounds_gen.sh
		sqlite3 $db_path < inbounds.sql
                echo -e "\e[34mAdded XTLS-Reality config entry into x-ui.db database\e[0m"
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

#Check for existing team_418 folder and clones repo (testing) with wget
function clone_repo() {
    if [[ -d "team_418" ]]; then
        cd team_418 || exit
        # Here you might want to fetch and unzip again or just rely on the existing content.
        # We're assuming that you want to fetch the newest content. 
        # So we'll remove the old files, fetch the new .zip and then unzip.
        rm -rf *
        wget https://github.com/torikki-tou/team418/archive/refs/heads/main.zip
        unzip main.zip
        mv team418-main/* .
        rm -rf team418-main main.zip
		echo -e "\e[34m team418 repository has been cloned\e[0m"
    else
        wget https://github.com/torikki-tou/team418/archive/refs/heads/main.zip
        unzip main.zip
        mkdir -p team_418
        mv team418-main/* team_418/
        cd team_418 || exit
        rm -rf ../team418-main ../testing.zip
		echo -e "\e[34m team418 repository has been cloned\e[0m"
    fi
}

#Check if user is root, halt if not
if ! isRoot; then
    echo "This script must be run as root"
    exit 1
fi

#Docker installation with checking for uuid and sqlite packages
echo -e "Checking for uuidgen package installed...."
check_uuidgen
echo -e "Checking for sqlite3 package installed...."
check_sqlite3
echo -e "Checking for Docker packages installed...."
check_docker
if [[ $? -ne 0 ]]; then
    read -p "Docker components are missing, would you like to install them? (y/n) (If not, you would have to install them manually) : " response
    if [[ $response == "y" ]]; then
        install_docker
		echo -e "\e[34mDocker packages were installed\e[0m"
    else
        echo "Aborting"
        exit 1
    fi
fi

#Checks for unzip package
echo -e "Checking for unzip package installed...."
check_unzip
#Clones team418 repo
echo -e "Cloning team_418 repository from Github..."
clone_repo
chmod +x inbounds_gen.sh

# Function to check existence of a variable in .env
function check_variable() {
    local var_name="$1"
    if ! grep -q "^$var_name=" .env; then
        return 1
    fi
    return 0
}

# Function to check for all the variables in .env
function check_all_variables() {
    local variables=("XUI_USERNAME" "XUI_PASSWORD" "XUI_PANEL_PORT" "XUI_HOSTNAME" "XUI_EMAIL" "TGTOKEN" "ADMINID")
    for var in "${variables[@]}"; do
        if ! check_variable "$var"; then
            return 1
        fi
    done
    return 0
}

# Check if all variables exist in .env
if check_all_variables; then
    read -p "Variables already exist in .env. Do you want to reinstall admin panel from scratch? (y/n): " response
    if [[ $response != "y" ]]; then
        echo "Aborting."
        exit 0
    fi
fi

echo -e "
          _  _   _  ___
         | || | / |( _ )
         | || |_| |/ _ \
         |__   _| | (_) |
            |_| |_|\___/ 
			"
echo -e "\e[32mWelcome to 3X-UI Docker + Traefik + TelegramBot installation script\e[0m"

read -p "Enter username for 3X-UI Panel: " usernameTemp
read -p "Enter password (only numbers and letters, no special characters): " passwordTemp
read -p "Enter port on which 3X-UI web admin panel would be available: " config_port
read -p "Enter your hostname (IP or Domain):" hostname_input
read -p "Enter your e-mail for certificate :" email_input
read -p "Enter your Telegram bot API token (use Tg BotFather):" tgtoken_input
read -p "Enter your Telegram admin profile (as @admin without @):" tgadminid_input

#Export variables to docker-compose
export XUI_USERNAME=$usernameTemp
export XUI_PASSWORD=$passwordTemp
export XUI_PANEL_PORT=$config_port
export XUI_HOSTNAME=$hostname_input
export XUI_EMAIL=$email_input
export TGTOKEN=$tgtoken_input
export ADMINID=$tgadminid_input

#Export variables to .env file
echo "XUI_USERNAME=$XUI_USERNAME" > .env
echo "XUI_PASSWORD=$XUI_PASSWORD" >> .env
echo "XUI_PANEL_PORT=$XUI_PANEL_PORT" >> .env
echo "XUI_HOSTNAME=$XUI_HOSTNAME" >> .env
echo "XUI_EMAIL=$XUI_EMAIL" >> .env
echo "TGTOKEN=$TGTOKEN" >> .env
echo "ADMINID=$ADMINID" >> .env

docker compose up -d
docker exec 3x-ui sh -c "/app/x-ui setting -username $usernameTemp -password $passwordTemp"
echo -e "username and password applied to 3X-UI Container"
sleep 1
docker restart 3x-ui
echo -e "3X-UI Docker container restarted"
sleep 3
#Adds default config for XTLS-Reality into x-ui.db if conditions met (prompt y/n)
check_inbounds_table

docker restart 3x-ui
echo -e "\e[32m3X-UI + Traefik + TelegramBot installation finished, XTLS-Reality default config added, admin panel is available on https://$hostname_input:$config_port\e[0m"

