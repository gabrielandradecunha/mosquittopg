#!/bin/bash

#user test
docker exec -it postgres_mosquitto psql -U postgres -d postgres -c "
INSERT INTO users (name, email, password, is_admin, created_at, updated_at)
VALUES ('Gabriel', 'gandradecortez50@gmail.com', 'gabriel', FALSE, NOW(), NOW());
"

#reserv test
docker exec -it postgres_mosquitto psql -U postgres -d postgres -c 'select * from reservatorios';docker exec -it postgres_mosquitto psql -U postgres -d postgres -c "
INSERT INTO reservatorios (nome, volume_maximo, volume_atual, ultima_atualizacao, descricao, user_id, created_at, updated_at)
VALUES ('Reservatório A', 10000.00, 5000.00, NOW(), 'Reservatório de teste', 1, NOW(), NOW());
"