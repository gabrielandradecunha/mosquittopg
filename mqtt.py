import psycopg2
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()
# mosquitto credentias
user = os.getenv('USER')
password = os.getenv('PASSWORD')

#DB
def conn_db():
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    database_url = -f"postgresql://{user}:{password}@{host}:{port}/{dbaname}"

    try:
        connection = psycopg2.connect(database_url)
        print("conexão com db estabelecida...")
    except psycopg2.Error as e:
        print(f"erro: {e}")


def update_db(table_id, new_vol):
    conn_db()
    cursor = connection.cursor()
    query = "UPDATE reservatorios SET volume_atual=%s WHERE nome=%s"

    try:
        cursor.execute(query, (new_vol, table_id))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Volume atualizado com sucesso para o reservatório {table_id}. Novo volume: {new_vol}")
        else:
            print(f"Nenhum reservatório encontrado com o nome {table_id}. Nenhuma atualização realizada.")
    except Exception as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


# mqtt
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code: {reason_code}")
    client.subscribe("reservatorio/volume")

def on_message(client, userdata, msg):
    print(f"Tópico: {msg.topic}")
    print(f"Conteudo: {type(msg.payload)}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set(user, password)

mqttc.connect("localhost", 1883, 60)

mqttc.loop_forever()
