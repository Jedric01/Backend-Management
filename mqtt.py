from paho.mqtt import client as mqtt_client
import json

class MQTTClient():

    # Connection Settings
    CLIENT_ID = 'Backend-Worker'
    # authentication
    # USERNAME = 'user'
    # PASSWORD = 'password'

    def __init__(self, broker_address, port):
        self.broker_address = broker_address
        self.port = port

    # Connect to mqtt and return a MQTT Client object
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        def on_disconnect(client, userdata, rc):
            print("Disconnect")
        # Set Connecting Client ID
        client = mqtt_client.Client(self.CLIENT_ID)
        # client.username_pw_set(username=, password)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.connect(self.broker_address, self.port)
        self.client = client

    def disconnet_mqtt(self):
        self.client.disconnect()

    # publish to a topic
    def publish(self, topic: str, msg: str):
        msg_count = 0
        print(msg)
        result = self.client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    # subscribes to a topic, with a MQTT Client attaches callback to process received messages
    def subscribe(self, topic, callback):
        # callback for messages received via subscribe
        def on_message(client, userdata, msg):
            # created_task = app.mongdb["db-test"].find_one(
            #     {"_id": new_status.inserted_id}
            # )
            # # TODO: validate message before inserting to db
            # new_status = app.mongodb["db-test"].insert_one(created_task)
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            client.disconnect()
            return msg


        # callback for processing received messages from the subscribed topic 
        self.client.subscribe(topic)
        self.client.on_message = on_message
        # TODO; Figure out loop, right now this command is blocking 
        self.client.loop_forever()