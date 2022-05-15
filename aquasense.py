from flask import Flask, render_template, url_for, Response, stream_with_context
from flask.wrappers import Response
from flask_bootstrap import Bootstrap
from decouple import config
import json
from datetime import datetime
from flask_moment import Moment
from mongodb_test import *

app = Flask(__name__)
moment = Moment(app)

bootstrap = Bootstrap(app)


def _datos(cur):
    try:
        cur.execute(
            'SELECT fecha_hora, agua_flujo FROM datos_dia WHERE id = (SELECT MAX(id) FROM datos_dia)')
        datos_tiempo_real = cur.fetchall()
        json_data = json.dumps(
            {'fecha': datos_tiempo_real[0][0].strftime("%d/%m/%Y %H:%M:%S"), 'numero1': datos_tiempo_real[0][1]})
    except:
        json_data = json.dumps(
            {'fecha':  datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'numero1': 0})
    yield f"data:{json_data}\n\n"
    
def _data_gauge(device_name):
    
    variables = devices_var(device_name)
    json_data = json.dumps({'temperature': float(variables.rt_temperature),
                            'humidity': float(variables.rt_humidity)})
    

    yield f"data:{json_data}\n\n"

@app.route('/')
def index():
    devices = devices_info()

    return render_template('index.html', devices=devices)


@app.route('/dashboard/<device_name>')
def dashboard(device_name):
    
    return render_template('dashboard.html', device_name=device_name)



@app.route('/graficas')
def graficas():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT agua_flujo, fecha_hora FROM datos_dia WHERE fecha_hora > DATE_ADD(NOW(), INTERVAL -10 HOUR)")
    flujo_dia = cur.fetchall()

    cur.execute(
        "SELECT  maximo_flujo, fecha FROM datos_semana")
    flujo_semana = cur.fetchall()
    
    cur.execute(
        "SELECT maximo_flujo FROM datos_semana WHERE week(fecha)=week(now())")
    flujo_semana_actual = cur.fetchall()
    print(flujo_semana_actual)
    
    
    return render_template('graficas.html', graficas="active",
                           flujo_dia=flujo_dia, flujo_semana=flujo_semana,
                           flujo_semana_actual=flujo_semana_actual)


@app.route('/tablas')
def tablas():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT * FROM datos_semana")
    valores = cur.fetchall()
    return render_template('tablas.html', tablas="active", valores=valores)

@app.route('/tiempo_real/<device_name>')
def flujo_tiempo_real(device_name):
    enviar = _data_gauge(device_name)
    
    return Response(stream_with_context(enviar), mimetype='text/event-stream')

@app.route('/predicciones')
def predicciones():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT * FROM datos_prediction")
    valores = cur.fetchall()

    return render_template('predicciones.html', predicciones="active", valores=valores)


if __name__ == "__main__":
    app.run(debug=True)
