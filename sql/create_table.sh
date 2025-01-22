#!/bin/bash

# cmd to execute script for create tables

docker exec -it postgres_mosquitto psql -U postgres -d postgres -f ./sql/test.sql