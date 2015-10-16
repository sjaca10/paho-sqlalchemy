import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, rc):
	print "Client connected with result {0}".format(rc)
	client.subscribe("mongodb/company/Position")
	client.subscribe("mysql/company/Position")
	client.subscribe("redis/company/Position")
	client.subscribe("postgresql/company/Position")

def on_subscribe(client, userdata, mid, granted_qos):
	print "Subscribed with Quality of Service {0}".format(granted_qos)

def on_publish(client, userdata, mid):
	print("Message published, completed transmition to the broker")

client              = mqtt.Client()
client.on_connect   = on_connect
client.on_subscribe = on_subscribe
client.on_publish   = on_publish

client.connect("localhost", 1883, 60)

my_position = dict(
    latitude  = 48.8587936,
    longitude = 2.2958711
)

client.publish("mysql/company/Position", payload = json.JSONEncoder().encode(my_position))
client.publish("postgresql/company/Position", payload = json.JSONEncoder().encode(my_position))
client.loop_forever()