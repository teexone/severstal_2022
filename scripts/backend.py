import time
from datetime import datetime
from io import BytesIO
from main import calculate as calc
from flask import Flask, request, send_file
import pandas as pd
from data import dictate, refine
from filters import by_name
from appformat.date import int_to_date
from external import get_data, get_indices
from permanent.permanent import order_date_column, order_price_column
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

data = refine('../data/severstal/datamon.xlsx')


@app.route('/indices')
def indices():
    return {'indices': get_indices()}, 200


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
            'x': list(map(lambda x: x.timestamp(), dct.keys())),
            'y': list(dct.values()),
            'name': "Цена товара"
        }, 200
    elif what == 'index':
        index = request.args.get('index')
        arr = get_data(index)
        keys = [[int_to_date(_[0]) for _ in x] for x in arr]
        values = [list(_[1] for _ in x) for x in arr]
        x = list(map(lambda x: time.mktime(x.timetuple()), keys[0]))
        y = []
        for i in range(len(values[0])):
            y.append(sum([values[j][i] for j in range(len(values))]) / len(values))
        return {'x': x, 'y': y}, 200


@app.route('/calculate')
def calculate():
    indices = request.args.getlist('include')
    method = request.args.get('method')
    product = request.args.get('product')
    date = int(request.args.get('date'))
    to_excel = bool(request.args.get('to_excel'))
    try:
        date = datetime.fromtimestamp(date / 1000).date()
    except ValueError:
        return 'cannot parse ISO format for date', 400

    if to_excel:
        df = calc(product, date, indices, method, return_steps=True)
        o = BytesIO()
        writer = pd.ExcelWriter(o)
        df.to_excel(writer, sheet_name='Prediction')
        writer.save()
        o.seek(0)
        return send_file(o, download_name=f'PredictionOutput_{date}', as_attachment=True), 200
    if indices is None or method is None or product is None or date is None:
        return '', 400
    result, error = calc(product, date, indices, method)
    return {'predicted': result[0], 'error': error}, 200


if __name__ == '__main__':
    app.run(port=5000)
