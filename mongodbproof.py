from errno import ELIBBAD
from mongoengine import *
from pkg_resources import require


connect(host="mongodb+srv://manuelmj:Ma1234567890@cluster0.9o8wd.mongodb.net/Be-caribeDatabase?retryWrites=true&w=majority")
class GraphData(EmbeddedDocument):
    temperature=DecimalField()
    humidity=DecimalField()

class Device(Document):
    device_name=StringField(unique=True, primary_key=True,max_length=50)
    rt_temperature=DecimalField(required=True)
    rt_humidity=DecimalField(required=True)
    graph_data=EmbeddedDocumentField(GraphData)


device_data={
    "device_name":"dispositivo1",
    "rt_temparature":20.0,
    "rt_humidity":20.0
    }

device=Device(device_name="Dispositivo1",rt_temperature=20.0,rt_humidity=20.0)
device.save()




