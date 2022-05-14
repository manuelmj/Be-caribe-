from mongoengine import *
from datetime import datetime
from decouple import config
import json

connect(host=config('MONGO_URI'))


class GraphData(EmbeddedDocument):
    temperature = DecimalField(required=True)
    humidity = DecimalField(requiered=True)
    date = DateTimeField(required=True, default=datetime.now)


class Device(Document):
    device_name = StringField(unique=True, max_length=50, required=True)
    last_update = DateTimeField(required=True)
    rt_temperature = DecimalField(required=True)
    rt_humidity = DecimalField(required=True)
    graph_data = ListField(EmbeddedDocumentField(GraphData))


def data_sender(device_name: str, rt_temperature: float, rt_humidity: float) -> None:
    try:
        device = Device.objects(device_name=device_name)
        print(device)
    except:
        device = Device(device_name=device_name,
                        rt_temperature=rt_temperature, rt_humidity=rt_humidity, last_update=datetime.now())
        device.save()
    else:
        device.update(last_update=datetime.now(),
                      rt_temperature=rt_temperature, rt_humidity=rt_humidity)


def devices_info() -> list:
    devices = Device.objects.exclude('graph_data').exclude(
        'rt_temperature').exclude('rt_humidity').exclude('id').to_json()
    return json.loads(devices)


def update_graph_data(device_name):
    device = Device.objects.get(device_name=device_name)
    graph_data = GraphData(
        temperature=device.rt_temperature, humidity=device.rt_humidity)
    device.graph_data.append(graph_data)
    device.save()
