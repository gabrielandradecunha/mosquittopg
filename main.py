import psycopg2
import paho.mqtt.client as mqtt
import os
import json
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('MOSQUITTO_USER')
password = os.getenv('MOSQUITTO_PASSWORD')
mqtt_host = os.getenv('MOSQUITTO_HOST')
mqtt_port = os.getenv('MOSQUITTO_PORT')
mqtt_topic = os.getenv('MOSQUITTO_TOPIC')

# DB
def update_db(table_id, new_vol):
    dbname = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    database_url = f"postgresql://{db_user}:{password}@{host}:{port}/{dbname}"

    try:
        connection = psycopg2.connect(database_url)
        print("Conexão com DB estabelecida...")
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return

    cursor = connection.cursor()
    query = "UPDATE reservatorios SET volume_atual=%s WHERE id=%s"

    try:
        cursor.execute(query, (new_vol, table_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Volume atualizado com sucesso para o reservatório {table_id}. Novo volume: {new_vol}")
        else:
            print(f"Nenhum reservatório encontrado com o ID {table_id}. Nenhuma atualização realizada.")
    except Exception as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
        connection.rollback()
    finally:
        cursor.close()
        if connection:
            connection.close()

# MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado com o código de resultado: {reason_code}")
    client.subscribe(mqtt_topic)

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s", rc)

def on_message(client, userdata, msg):
    print(f"Tópico: {msg.topic}")

    json_string = msg.payload
    data = json.loads(json_string)

    print(f"id: {data['id']} e volume: {data['volume']}")

    update_db(data['id'], data['volume'])

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# tls
# mqttc.tls_set()

mqttc.username_pw_set(user, password)
mqttc.connect(str(mqtt_host), int(mqtt_port), 60)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_forever()