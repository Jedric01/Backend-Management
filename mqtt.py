from paho.mqtt import client as mqtt_client
import json
import time

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
        # client.on_connect = on_connect
        # client.on_disconnect = on_disconnect
        client.connect(self.broker_address, self.port)
        self.client = client

    def disconnect_mqtt(self):
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
            # signal to calling thread, that message has been received

            return msg


        # callback for processing received messages from the subscribed topic 
        self.client.subscribe(topic)
        self.client.on_message = on_message
        # TODO; Figure out loop, right now this command is blocking 

        self.client.loop_start()

    # subscribe and waits 
    def sub_and_wait(self, topic, timeout):
        stop = False
        # connect to mqtt
        self.connect_mqtt()
        response = None
        def on_message(client, userdata, msg):
            nonlocal stop
            nonlocal response
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            response = msg
            stop = True

        self.client.subscribe(topic)
        self.client.on_message = on_message
        current_time = time.time()
        
        # loop for the alloted time or when message has been received
        while time.time() - current_time < timeout and not stop:
            print('looping', time.time() - current_time)
            self.client.loop()
        self.client.loop_stop()
        self.client.unsubscribe(topic)
        # disconnect 
        self.disconnect_mqtt()
        
        return response

        