from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request, json, abort, Response
from models import data_models

load_dotenv()

app = Flask(__name__)

data_models.issuers.reader()  # Что бы при запуске сервера все данные загрузились сразу


@app.route('/search', methods = ['GET'])
def api_search():
    issuers = data_models.issuers.search(dict({
        'ticker': request.args.get('ticker'),
        'number': request.args.get('number'),
    }))

    if len(issuers) <= 0:
        abort(404)

    return Response(
        status = 200,
        mimetype = "application/json",
        response = json.dumps({
            'success': True,
            'data':    {
                'issuers': issuers,
            },
            'errors':  [],
        })
    )


@app.route('/all', methods = ['GET'])
def api_all():
    return Response(
        status = 200,
        mimetype = "application/json",
        response = json.dumps({
            'success': True,
            'data':    {
                'issuers': data_models.issuers.issuers,
            },
            'errors':  [],
        })
    )


@app.errorhandler(404)
def page_not_found(e):
    response = Response(json.dumps({
        'success': False,
        'data':    [],
        'errors':  [
            {'message': str(e), 'code': 'BadRequest'}
        ],
    }), status = 404, mimetype='application/json')

    return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = os.getenv('HTTP_PORT'))  # debug=True
