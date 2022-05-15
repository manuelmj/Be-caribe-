from mongoengine import *
from datetime import datetime, timedelta
from decouple import config


connect(host=config('MONGO_URI'))


class GraphData(Document):
    device_name = StringField(required=True, max_length=50)
    temperature = DecimalField(required=True)
    humidity = DecimalField(requiered=True)
    date = DateTimeField(required=True, default=datetime.utcnow())


class Device(Document):
    device_name = StringField(unique=True, max_length=50, required=True)
    last_update = DateTimeField(required=True)
    rt_temperature = DecimalField(required=True)
    rt_humidity = DecimalField(required=True)


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
    devices = Device.objects.exclude(
        'rt_temperature').exclude('rt_humidity').exclude('id')
    return devices


def devices_var(device_name):
    devices = Device.objects(device_name=device_name).exclude(
        'device_name').exclude('last_update').exclude('id').get()
    return devices


def devices_graph(device_name: str, date_from: datetime, date_to: datetime) -> list:
    graph_data = GraphData.objects(
        device_name=device_name, date__gte=date_from, date__lte=date_to).exclude('id').exclude('device_name')
    return graph_data


def graph_data_update(device_name: str) -> None:
    device = Device.objects(device_name=device_name).exclude(
        'id').exclude('last_update').get()
    graph_data = GraphData(device_name=device_name,
                           temperature=device.rt_temperature, humidity=device.rt_humidity)
    graph_data.save()

<<<<<<< HEAD

def delete_device(device_name: str) -> None:
    device = Device.objects(device_name=device_name).get()
    graph_data = GraphData.objects(device_name=device_name)
    if device.last_update < datetime.utcnow() - timedelta(weeks=3):
        device.delete()
        graph_data.delete()
=======
>>>>>>> 4f1735c86c79fdd9be4a65beca4b7a0b82bb4e60
