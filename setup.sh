#!/bin/bash

# cmd resume

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -v

mv .env.examble .env

touch mosquitto/config/pass
sudo chmod 0700 mosquitto/config/pass
docker-compose up -d

# db
sudo chmod -R +x sql/
sudo sql/create_table.sh
sudo sql/insert_table.sh

python3 main.py