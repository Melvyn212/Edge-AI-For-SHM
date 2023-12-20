#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y apt utils
sudo apt-get install -y ansible
sudo apt-get install -y jq


ansible --version
PLAYBOOK_PATH="set_up_jnano_executable.yml"
ansible-playbook $PLAYBOOK_PATH -i "localhost," --connection=local


sudo apt-get install -y  python3-matplotlib

#taper ./set_up_jnano.sh
