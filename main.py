import os
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv('MOSQUITTO_USER')
password = os.getenv('MOSQUITTO_PASSWORD')
mqtt_host = os.getenv('MOSQUITTO_HOST')
mqtt_port = os.getenv('MOSQUITTO_PORT')
mqtt_topic = os.getenv('MOSQUITTO_TOPIC')

db_url = os.getenv('DB_URL')  
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Reservatorio(Base):
    __tablename__ = 'reservatorios'
    id = Column(Integer, primary_key=True)
    volume_atual = Column(Float)

    def __repr__(self):
        return f"<Reservatorio(id={self.id}, volume_atual={self.volume_atual})>"

def update_db(table_id, new_vol):
    try:
        reservatorio = session.query(Reservatorio).filter_by(id=table_id).first()
        
        if reservatorio:
            reservatorio.volume_atual = new_vol
            session.commit()
            print(f"Volume atualizado com sucesso para o reservatório {table_id}. Novo volume: {new_vol}")
        else:
            print(f"Nenhum reservatório encontrado com o ID {table_id}. Nenhuma atualização realizada.")
    except Exception as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
        session.rollback()

# MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado com o código de resultado: {reason_code}")
    client.subscribe(mqtt_topic)

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code: {rc}")

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