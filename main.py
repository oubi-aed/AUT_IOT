import configparser#
from database import Database

# 1. ConfigParser-Objekt erstellen und Datei laden
config = configparser.ConfigParser()
config.read('config.ini')

# 2. Werte auslesen
mqtt_user = config.get('MQTT', 'username')
mqtt_pass = config.get('MQTT', 'password')
mqtt_host = config.get('MQTT', 'host')
mqtt_port = config.getint('MQTT', 'port')

# 3. Datenbank initialisieren
db = Database(db_path='db.json')

# 4. mqtt lesen