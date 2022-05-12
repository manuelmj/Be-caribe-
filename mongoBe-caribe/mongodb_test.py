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
    activity = BooleanField(default=True)
    rt_temperature = DecimalField(required=True)
    rt_humidity = DecimalField(required=True)
    graph_data = ListField(EmbeddedDocumentField(GraphData))


def data_sender(device_name: str, rt_temperature: float, rt_humidity: float) -> None:
    try:
        device = Device(device_name=device_name,
                        rt_temperature=rt_temperature, rt_humidity=rt_humidity)
        device.save()
    except NotUniqueError:
        device = device.objects.get(device_name=device_name)
        device.rt_humidity = rt_humidity
        device.rt_temperature = rt_temperature
        device.save()
