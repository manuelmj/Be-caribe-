from mongoengine import *
from datetime import datetime
from decouple import config

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


def devices_info():
    devices = Device.objects.exclude('graph_data').exclude(
        'rt_temperature').exclude('rt_humidity').exclude('id')

    return devices

def devices_var(device_name):
    devices = Device.objects(device_name=device_name).exclude('graph_data').exclude(
        'device_name').exclude('last_update').exclude('id').get()
    return devices
