import paho.mqtt.client as mqtt
import configparser

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database



# 1. ConfigParser-Objekt erstellen und Datei laden
config = configparser.ConfigParser()
config.read('config.ini')

# 2. Werte auslesen
user = config.get('MQTT', 'username')
password = config.get('MQTT', 'password')
broker = config.get('MQTT', 'host')
port = config.getint('MQTT', 'port')

# 3. Datenbank initialisieren
db = Database(db_path='db.json')

topic = "iot1/teaching_factory/#"
payload = "on"



## get data from broker

# create function for callback
def on_message(client, userdata, message):
    print("message received:")
    db.insert({
        'topic': message.topic,
        'payload': message.payload.decode('utf-8'),
    })


# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(user, password)

# assign function to callback
mqttc.on_message = on_message                          

# establish connection
mqttc.connect(broker, port)

# subscribe
mqttc.subscribe(topic, qos=0)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
#mqttc.loop_forever()

while True:
    mqttc.loop(0.5)