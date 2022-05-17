from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import json
import time 
from datetime import datetime 
from  decouple import Config
from mongodb_test import data_sender, delete_device 
from mongoengine import *

connected_flag = False
counter = 0
messages_time = dict() 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
    else:
        print("unexpected disconenection. resultcode "+ str(rc))


def on_message(client, userdata, msg):
    global data 


    data_json = str(msg.payload, 'utf-8')
    data = json.loads(data_json)
    messages_time[data["device_name"]] = datetime.utcnow() 

    try:
        data_sender(data["device_name"],data["rt_temperature"],data["rt_humidity"])
    except:
        pass


def unexpected_disconnect():
    for message in messages_time.keys(): 
        if  messages_time[message] < ( datetime.utcnow() - timedelta(seconds=10) ):
            data_sender(data[message],0,0)
            if messages_time[message] <  datetime.utcnow() - timedelta(weeks=3):
                delete_device(message)
                messages_time.pop(message)



def run():
    counter
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
  # client.loop_forever()
    client.loop_start()

    while True:
      
        time.sleep(5)
        unexpected_disconnect()
    

    client.loop_stop()


if __name__ == '__main__':
   run()
