#!/usr/bin/with-contenv bashio

echo "Start Object Detection Extension!"

#variable
CAMERA_ENTITY=$(bashio::config 'camera_entity')
USER_TOKEN=$(bashio::config 'user_token')

#set environment
export CAMERA_ENTITY=$CAMERA_ENTITY
export HA_TOKEN=$USER_TOKEN

#logging
echo "the bootnode address is => ${CAMERA_ENTITY}"
echo "the bootnode port is => ${USER_TOKEN}"

#execute main program
source ./venv/Scripts/activate
python app.py