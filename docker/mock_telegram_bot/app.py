import json
from os import environ

from flask import Flask, jsonify, request

app = Flask(__name__)

REQUESTS = []


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'pass'})


@app.route('/<token_id>/sendMessage', methods=['POST'])
def send_message(token_id: str):
    del token_id
    REQUESTS.append(json.loads(request.data.decode('utf-8')))
    return jsonify({'ok': True, 'result': True})


@app.route('/dev/requests', methods=['GET'])
def requests():
    return jsonify(REQUESTS)


@app.route('/dev/requests/last', methods=['GET'])
def requests_last():
    return jsonify(REQUESTS[-1])


@app.route('/dev/requests/clear', methods=['GET'])
def requests_clear():
    REQUESTS.clear()
    return jsonify('Requests cleared')


if __name__ == '__main__':
    app.run(host=environ['APP_HOST'], port=environ['APP_PORT'])
