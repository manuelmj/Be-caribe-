from datetime import datetime
from enum import unique
from unicodedata import decimal
import paho.mqtt.client as mqtt
import json
from  decouple import Config
from mongodb_test import data_sender 
from mongoengine import *

connected_flag = False
counter = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
    else:
        print("unexpected disconenection. resultcode "+ str(rc))

#########################################33
def on_message(client, userdata, msg):
    
    global connected_flag
    global counter 
    counter = 0
    connected_flag = True

    data_json = str(msg.payload, 'utf-8')
    data = json.loads(data_json)

    try:
        data_sender(data["device_name"],data["rt_temperature"],data["rt_humidity"])
    except:
        pass

############################

def unexpected_disconnect():
   data_sender(data["device_name"],0.0,0.0)

def run():
    global counter
    global connected_flag

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
  # client.loop_forever()
    client.loop_start()

    while True:
        if(connected_flag is True):
            time.sleep(1)
            counter += 1
        if(counter >= 5):
            unexpected_disconnect()
            connected_flag = False
            counter = 0
    client.loop_stop()


if __name__ == '__main__':
   run()
