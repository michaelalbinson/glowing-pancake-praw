from client.util.HTMLUtil import HTMLUtil
from flask import request
from api.local_stocks.TickerWrapper import TickerWrapper
from cli.update_ticker import update_ticker


def stock_search_routes(app):
    @app.route('/stock-search')
    def get_stock_search():
        return HTMLUtil.get_template('stock-search.html')

    @app.route('/stock-search/ticker', methods=['GET', 'PUT'])
    def get_stock_ticker():
        ticker = request.args.get('t', default='NOT_FOUND', type=str)
        if ticker is None:
            return ""

        if request.method == 'PUT':
            update_ticker([ticker.upper()])

        wrap = TickerWrapper.get(ticker.upper())
        if wrap is None:
            return ""

        return wrap.to_json()
