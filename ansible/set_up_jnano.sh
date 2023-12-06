#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y apt utils
sudo apt-get install -y ansible
ansible --version
PLAYBOOK_PATH="set_up_jnano_executable.yml"
ansible-playbook $PLAYBOOK_PATH -i "localhost," --connection=local

#taper ./set_up_jnano.sh