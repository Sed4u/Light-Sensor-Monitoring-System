import paho.mqtt.client as mqtt
import random
import time
import json
import warnings
import psycopg2

warnings.filterwarnings("ignore", category=DeprecationWarning)

BROKER = "mosquitto"
PORT = 1883
TOPIC = "senzor/lumina"

PG_HOST = "postgres"
PG_PORT = 5432
PG_DB = "dbmds"
PG_USER = "mds"
PG_PASS = "mdspass"

def get_user_ids():
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASS
        )
        cur = conn.cursor()
        cur.execute("SELECT id FROM \"user\";")
        user_ids = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return user_ids
    except Exception as e:
        print(f"Could not fetch user ids: {e}")
        return []

def get_fake_lux():
    return round(random.uniform(100.0, 1000.0), 2)

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    user_ids = get_user_ids()
    for user_id in user_ids:
        lux = get_fake_lux()
        message = {
            "lux": lux,
            "timestamp": time.time(),
            "user_id": user_id
        }
        client.publish(TOPIC, json.dumps(message))
        print(f"Trimis: {message}")
    time.sleep(5)