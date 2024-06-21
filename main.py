from functools import wraps
from gevent.pywsgi import WSGIServer

import jwt
import requests
from flask import Flask, render_template, request, jsonify

from config import APP1_OLYMPUS_BUNDLE, BOT_TOKEN_OLYMPUS_APP1
from data.UserRepository import UserRepository

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check_db', methods=["POST"])
def chekc_db():
    request_data = request.get_json()
    if not request_data:
        return 'reqest is None', 400
    user = request_data.get("user", {})
    params = request_data.get("params", {})

    if not user:
        return 'User not exists', 400

    user_id = user.get("id", None)
    username = user.get("username", None)
    first_name = user.get("first_name", None)
    language_code = user.get("language_code", None)
    client_url = params.get("client_url", None)
    bundle = params.get("bundle", None)

    print(user)
    print(client_url)
    print(bundle)

    if bundle == APP1_OLYMPUS_BUNDLE:
        if not UserRepository().get_user_app1_olympus(user_id):
            if not UserRepository().add_user_app1_olympus(user_id, username, first_name, language_code, client_url):
                return 'Can`t add user to bot`s table', 400
            else:
                send_message(user_id, "Hello, Welcome to start game press 'Play' or /start", bundle)
    else:
        return 'Bot with bundle not exists', 400

    if not UserRepository().get_user(user_id):
        if not UserRepository().add_user(user_id, username, first_name, language_code):
            return 'User can`t add to all users table', 400

    return 'OK', 200


def send_message(chat_id, message, bundle):
    if bundle == APP1_OLYMPUS_BUNDLE:
        bot_token = BOT_TOKEN_OLYMPUS_APP1
    else:
        return

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    requests.post(url, data=payload)


if __name__ == '__main__':
    # app.run()
    http_server = WSGIServer(("0.0.0.0", 5030), app)
    http_server.serve_forever()
