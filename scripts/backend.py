import time
from datetime import datetime
from io import BytesIO
from main import calculate as calc
from flask import Flask, request, send_file
import pandas as pd
from data import dictate, refine
from filters import by_name
from external import get_data, get_indices
from permanent.permanent import order_date_column, order_price_column
from flask_cors import CORS

from appparser.IndicesParserModule.IndicesParserModule import IndicesParserModule

import numpy as np

app = Flask(__name__)
cors = CORS(app)

data = refine('../data/severstal/datamon.xlsx')
external = '../data/external/indices.xlsx'


@app.route('/indices')
def indices():
    return {'indices': get_indices()}, 200


@app.route("/top")
def top():
    return {
        'toplist': [_[0] for _ in pd.read_excel('../data/severstal/toplist.xlsx').to_numpy().tolist()]
        }, 200


@app.route("/plot")
def plot():
    what = request.args.get('what')
    if what == 'price':
        product = request.args.get('product')
        df = by_name(data, product, columns=[order_date_column, order_price_column])
        dct = dictate(df, order_date_column, order_price_column)
        return {
            'x': list(map(lambda x: x.timestamp(), dct.keys())),
            'y': list(dct.values()),
            'name': "Цена товара"
        }, 200
    elif what == 'index':
        index = request.args.get('index')
        index = IndicesParserModule(external, index)
        arr = index.get_data()
        keys = list(map(lambda x: int(time.mktime(x.timetuple())), arr.keys()))
        values = list(map(np.mean, arr.values()))
        return {'x': keys, 'y': values}, 200


@app.route('/calculate')
def calculate():
    indices = request.args.getlist('include')
    product = request.args.get('product')
    date = int(request.args.get('date'))
    to_excel = bool(request.args.get('to_excel'))
    try:
        date = datetime.fromtimestamp(date / 1000).date()
    except ValueError:
        return 'cannot parse ISO format for date', 400

    p_l, p_r, df = calc(product, date, indices)
    if to_excel:
        o = BytesIO()
        writer = pd.ExcelWriter(o)
        df.to_excel(writer, sheet_name='Prediction')
        writer.save()
        o.seek(0)
        return send_file(o, attachment_filename=f'PredictionOutput_{date}', as_attachment=True), 200
    if indices is None or product is None or date is None:
        return '', 400
    return {'left': float(p_l), 'right': float(p_r)}, 200


if __name__ == '__main__':
    app.run(port=5000)
