from datetime import datetime
from scripts.app.main import calculate as calc
from flask import Flask, request
import pandas as pd
from scripts.data import dictate, refine
from scripts.filters import by_name
from scripts.permanent.permanent import *
from scripts.app_format.date import int_to_date
from scripts.external import get_data, Indices
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

data = refine('data/severstal/datamon.xlsx')


@app.route('/indices')
def indices():
    return {
        'indices': {
            'Бензин': Indices.gas,
            'Сталь': Indices.steel,
            'Стальной прокат': Indices.metal,
            'Дизель': Indices.disel,
            'Автотранспорт': Indices.vehicles,
            'Станки':  Indices.machines,
            'Стальные профили': Indices.profiles,
            'Цельнокатаные колёса': Indices.rails,
            'Железная руда': Indices.ore,
        }
    }, 200


@app.route("/top")
def top():
    return {
        'toplist': [_[0] for _ in pd.read_excel('data/severstal/toplist.xlsx').to_numpy().tolist()]
        }, 200


@app.route("/plot")
def plot():
    what = request.args.get('what')
    if what == 'price':
        product = request.args.get('product')
        df = by_name(data, product, columns=[order_date_column, order_price_column])
        dct = dictate(df, order_date_column, order_price_column)
        return {
            'x': list(dct.keys()),
            'y': list(dct.values())
        }, 200
    elif what == 'index':
        index = request.args.get('index')
        arr = get_data(index)
        keys = [[int_to_date(_[0]) for _ in x] for x in arr]
        return {'x': keys, 'y': [list(_[1] for _ in x) for x in arr]}, 200


@app.route('/calculate')
def calculate():
    indices = request.args.getlist('include')
    method = request.args.get('method')
    product = request.args.get('product')
    date = request.args.get('date')
    print(indices)
    if indices is None or method is None or product is None or date is None:
        return '', 400
    try:
        date = datetime.fromisoformat(date).date()
    except ValueError:
        return 'cannot parse ISO format for date', 400
    return {'predicted': calc(product, date, indices, method)[0]}, 200


if __name__ == '__main__':
    app.run(port=5000)
