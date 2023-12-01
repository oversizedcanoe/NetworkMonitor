import paho.mqtt.client as mqtt
from logger import log

class MqttClient:
    def __init__(self, client_id: str):
        log("client id set to " + client_id)
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log

        self.client.connect("localhost")
        
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_start()
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe('\'test/topic\'')

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print('message received')
        try:
            print(msg.topic+" "+str(msg.payload))
        except BaseException as e:
            print('exception')
            print(str(e))

    def on_log(client, userdata, level, buf):
        print(f"Log: {buf}")

    def publish(self, topic: str , data: any):
        self.client.publish(topic, data)




