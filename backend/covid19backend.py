#!/usr/bin/env python

import datetime as dt
import json

#import autokeras
import tensorflow.keras as keras

from flask import Flask
from flask import request
from flask_cors import CORS


WINDOW_LEN = 36


class COVID19Predictor:
    def __init__(self):
        with open('model/data.json', 'rt') as f:
            self._data = json.load(f)

        self._model = keras.models.load_model('model/model.tf')

    def data(self):
        return {'data': self._data}

    def predict(self, country, start_date):
        start_date = dt.datetime.strptime(start_date, '%m-%d-%Y')

        x = [v for v in self._data if (v['country'] == country) and (dt.datetime.strptime(v['date'], '%m/%d/%y') >= start_date)][:WINDOW_LEN]
        x = [v['deaths'] for v in x] + [v['recoveries'] for v in x] + [v['cases'] for v in x]

        return float(self._model.predict([x])[0][0])

def create_app():
    app = Flask(__name__)
    CORS(app)

    controller = COVID19Predictor()

    @app.route('/data', methods=['GET'])
    def data():
        return controller.data()

    @app.route('/predict/<country>/<startDate>', methods=['GET'])
    def predict(country, startDate):
        prediction = controller.predict(country, startDate)

        return {'data': prediction}

    return app
