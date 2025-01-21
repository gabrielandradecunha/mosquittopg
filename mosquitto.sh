#/bin/bash

# publicando topico de teste

sudo docker exec -it mosquitto mosquitto_pub -h localhost -p 1883 -t "reservatorio/volume" -m '{"id": 1, "volume": 5000.00}' -u "laboratorio" -P "teste"
