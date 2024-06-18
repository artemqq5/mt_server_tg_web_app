from functools import wraps
from gevent.pywsgi import WSGIServer

import jwt
import requests
from flask import Flask, render_template, request, jsonify

from config import BOT_TOKEN
from data.UserRepository import UserRepository

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check_db', methods=["POST"])
def chekc_db():
    request_data = request.get_json()
    if not request_data:
        return 400
    user = request_data.get("user", None)
    params = request_data.get("params", None)
    if not user or not params:
        return 400
    
    if not UserRepository().get_user(user['id']):
        if not UserRepository().add_user(user['id'], user['username'], user['first_name'], user['language_code'], params):
            return 400
        else:
            send_message(user['id'], "Hello, Welcome to start game press 'Play'")

    print(user)
    print(params)

    return 'OK', 200


def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == '__main__':
    # app.run()
    http_server = WSGIServer(("0.0.0.0", 80), app)
    http_server.serve_forever()
