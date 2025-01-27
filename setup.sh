#!/bin/bash

# commands to easy and test setup 

# general python config
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -v

# .env for credentials
mv .env.example .env

# mosquitto
cd mosquitto/config/
touch pass
cd ../../
sudo chmod 0700 mosquitto/config/pass
docker-compose up -d
sudo ./genpass.sh

# db
sudo chmod -R +x sql/
sudo sql/setupdb.sh

python3 main.py

# publish test topic (optional)
# sudoo ./pub.sh