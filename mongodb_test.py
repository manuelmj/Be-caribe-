from mongoengine import *
from datetime import datetime, timedelta
from decouple import config


connect(host=config('MONGO_URI'))


class GraphData(EmbeddedDocument):
    temperature = DecimalField(required=True)
    humidity = DecimalField(requiered=True)
    date = DateTimeField(required=True, default=datetime.utcnow())


class Device(Document):
    device_name = StringField(unique=True, max_length=50, required=True)
    last_update = DateTimeField(required=True)
    rt_temperature = DecimalField(required=True)
    rt_humidity = DecimalField(required=True)
    graph_data = ListField(EmbeddedDocumentField(GraphData))


def data_sender(device_name: str, rt_temperature: float, rt_humidity: float) -> None:
    try:
        device = Device.objects.get(device_name=device_name)
        device.validate()
    except:
        device = Device(device_name=device_name,
                        rt_temperature=rt_temperature, rt_humidity=rt_humidity, last_update=datetime.utcnow())
        device.save()
    else:
        device.update(last_update=datetime.utcnow(),
                      rt_temperature=rt_temperature, rt_humidity=rt_humidity)


def devices_info():
    devices = Device.objects.exclude('graph_data').exclude(
        'rt_temperature').exclude('rt_humidity').exclude('id')
    return devices


def devices_var(device_name):
    devices = Device.objects(device_name=device_name).exclude('graph_data').exclude(
        'device_name').exclude('last_update').exclude('id').get()
    return devices


def devices_graph(device_name: str, date_from: datetime) -> list:
    raw_query = {'device_name': device_name,
                 'graph_data.date': {'$gte': date_from}}
    device = Device.objects(__raw__=raw_query).exclude('device_name').exclude(
        'last_update').exclude('id').exclude('rt_temperature').exclude('rt_humidity').get()
    return device


def graph_data_update(device_name: str) -> None:
    device = Device.objects(device_name=device_name).get()
    graph_data = GraphData(
        temperature=device.rt_temperature, humidity=device.rt_humidity)
    device.graph_data.append(graph_data)
    device.save()
