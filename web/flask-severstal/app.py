from datetime import datetime
from scripts.app.main import calculate as calc
from flask import Flask, request
import pandas as pd

app = Flask(__name__)


@app.route("/top")
def top():
    return {
        'toplist': [_[0] for _ in pd.read_excel('data/severstal/toplist.xlsx').to_numpy().tolist()] }, 200


@app.route('/calculate')
def calculate():
    indices = request.args.get('include')
    method = request.args.get('method')
    product = request.args.get('product')
    date = request.args.get('date')
    if indices is None or method is None or product is None or date is None:
        return '', 400
    if not isinstance(indices, list):
        return 'indices should be list', 400
    if not isinstance(method, str):
        return 'method should be string', 400
    if not isinstance(product, str):
        return 'product should be string', 400
    if not isinstance(date, str):
        return 'date should be iso formatted string', 400

    try:
        date = datetime.fromisoformat(date)
    except ValueError:
        return 'cannot parse ISO format for date', 400

    return calc(product, date, indices, method), 200


if __name__ == '__main__':
    app.run()
