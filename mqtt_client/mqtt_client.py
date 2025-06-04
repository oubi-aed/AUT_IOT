import paho.mqtt.client as mqtt
import configparser
from database import Database

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

topic = "iot1/teachingfactory"
payload = "on"

#send data to broker
def send_data_to_broker(topic, payload):

    # create function for callback
    def on_publish(client, userdata, flags, reasonCode, properties):
        print("data published \n")

    # create client object
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(user, password)              

    # assign function to callback
    mqttc.on_publish = on_publish                          

    # establish connection
    mqttc.connect(broker,port)                                 

    # publish
    return_code = mqttc.publish(topic, payload)

    mqttc.disconnect()



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