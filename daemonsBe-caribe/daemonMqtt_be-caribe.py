from datetime import datetime
from enum import unique
import time
from unicodedata import decimal
import paho.mqtt.client as mqtt
import json
import requests
from  decouple import config
from guardar_mqtt_db import cargarDB
from mongoengine import *

connected_flag = False
counter = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        print(probando) 
    else:
        print("unexpected disconenection. resultcode "+ str(rc))


def on_message(client, userdata, msg):
    global connected_flag
    global counter 
    counter = 0
    connected_flag = True

    valores_json = str(msg.payload, 'utf-8')
    valores = json.loads(valores_json)
    valores["fecha_hora"]=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(valores["fecha_hora"])
   

    try:
        cargarDB(valores)
    except:
        pass


def unexpected_disconnect():
    valores["fecha_hora"]=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    valores["flujo_agua"]=0
   # cargarBD(valores)


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
