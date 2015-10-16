from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Position import Position
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, rc):
	print "Client connected with result {0}".format(rc)
	client.subscribe("mysql/company/Position")
	client.subscribe("postgresql/company/Position")

def on_subscribe(client, userdata, mid, granted_qos):
	print "Subscribed with Quality of Service {0}".format(granted_qos)

def on_message(client, userdata, msg):
	print "Message received"
	data = msg.topic.split("/")
	client.insert(data[0], data[1], data[2], msg.payload)

def insert(dbms, database, table, payload):
	print "Information will insert on database {0} in table {1} at {2}".format(database, table, dbms)
	data = json.JSONDecoder().decode(payload)

	if dbms == "mysql":
		engine = create_engine('mysql+mysqldb://root:root@localhost/'+database,
			encoding = 'UTF-8', echo = False)
		client.sql(engine, table, data)
	elif dbms == "postgresql":
		engine = create_engine('postgresql+psycopg2://companyuser:companyuser@localhost/'+database,
			encoding = 'UTF-8', echo = False)
		client.sql(engine, table, data)
	else:
		print "Unsupported DBMS"

def sql(engine, table, data):
	Session = sessionmaker(bind = engine)

	# position = Position(latitude = data["latitude"], longitude = data["longitude"])
	# position = Position(**data)
	position = eval(table)(**data)

	session = Session()
	session.add(position)
	session.commit()

client              = mqtt.Client()
client.on_connect   = on_connect
client.on_subscribe = on_subscribe
client.on_message   = on_message
client.insert       = insert
client.mongo        = mongo
client.sql          = sql

client.connect("localhost", 1883, 60)
client.loop_forever()