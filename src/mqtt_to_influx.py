import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", category=DeprecationWarning)

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
TOKEN = os.getenv("INFLUX_TOKEN", "mds-token")
ORG = os.getenv("INFLUX_ORG", "mds")
BUCKET = os.getenv("INFLUX_BUCKET", "lumina")

client_influx = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)

BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "senzor/lumina")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with code:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        print("Raw payload:", msg.payload)
        payload = json.loads(msg.payload.decode())
        lux = float(payload["lux"])
        timestamp = payload["timestamp"]
        user_id = int(payload.get("user_id", 0))
        
        point = Point("lumina") \
            .tag("user_id", user_id) \
            .field("lux", lux) \
            .time(int(timestamp * 1e9))

        write_api.write(bucket=BUCKET, org=ORG, record=point)
        print(f"Saved to Influx: {lux} lux at {datetime.fromtimestamp(timestamp)} for user {user_id}")
    except Exception as e:
        print("Error:", e)

client_mqtt = mqtt.Client(protocol=mqtt.MQTTv311)
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

client_mqtt.connect(BROKER, PORT, 60)
client_mqtt.loop_forever()