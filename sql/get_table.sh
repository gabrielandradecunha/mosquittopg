#!/bin/bash

docker exec -it postgres_mosquitto psql -U postgres -d postgres -c 'select * from reservatorios';