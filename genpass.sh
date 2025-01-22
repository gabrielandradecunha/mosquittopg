#!/bin/bash

# generate password in container cmd

sudo docker exec -it mosquitto mosquitto_passwd -c /mosquitto/config/pass gabriel