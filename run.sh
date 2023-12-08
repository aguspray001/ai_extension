#!/usr/bin/with-contenv bashio

echo "Start Object Detection Extension!"

#variable
CAMERA_ENTITY=$(bashio::config 'camera_entity')
USER_TOKEN=$(bashio::config 'user_token')
OB_MODEL=$(bashio::config 'user_token')
#set environment
export CAMERA_ENTITY=$CAMERA_ENTITY
export HA_TOKEN=$USER_TOKEN
export OB_MODEL=$OB_MODEL

#logging
echo "camera entity => ${CAMERA_ENTITY}"
echo "user token => ${USER_TOKEN}"
echo "ob model => ${OB_MODEL}"

#execute main program
# source ./venv/Scripts/activate
python app.py