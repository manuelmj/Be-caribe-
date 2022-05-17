from operator import imod
from flask import Flask, redirect, render_template, session, url_for, Response, stream_with_context
from flask.wrappers import Response
from flask_bootstrap import Bootstrap
from datetime import datetime, time
import json
from flask_moment import Moment
from decouple import config
from mongodb_test import *
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = config('SECRET_KEY')

class DateForm(FlaskForm):
    date_from = DateField('Datos desde:',validators=[DataRequired()])
    date_to = DateField('hasta:',validators=[DataRequired()])
    submit = SubmitField('Buscar')


def _data_gauge(device_name):
    
    variables = devices_var(device_name)
    json_data = json.dumps({'temperature': float(variables.rt_temperature),
                            'humidity': float(variables.rt_humidity)})
    
    yield f"data:{json_data}\n\n"


@app.route('/')
def index():
    devices = devices_info()

    return render_template('index.html', devices=devices)


@app.route('/dashboard/<device_name>', methods=['GET', 'POST'])
def dashboard(device_name):
    form = DateForm()
    if form.validate_on_submit():
        data = devices_graph(device_name, 
                            datetime.combine(form.date_from.data, time()),
                            datetime.combine(form.date_to.data, time()))

        return render_template('dashboard.html', device_name=device_name, data=data, form=form)
    
    return render_template('dashboard.html', device_name=device_name, 
                           form=form, data=[])

@app.route('/tiempo_real/<device_name>')
def flujo_tiempo_real(device_name):
    enviar = _data_gauge(device_name)
    
    return Response(stream_with_context(enviar), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
