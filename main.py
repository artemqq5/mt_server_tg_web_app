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
    user = request_data.get("user", {})
    params = request_data.get("params", {})

    if not user or not params:
        return 400

    user_id = user.get("id", None)
    username = user.get("username", None)
    first_name = user.get("first_name", None)
    language_code = user.get("language_code", None)
    client_url = params.get("client_url", None)
    bundle = params.get("bundle", None)

    if not UserRepository().get_user(user_id):
        if not UserRepository().add_user(user_id, username, first_name, language_code, params):
            return 400
        else:
            send_message(user_id, "Hello, Welcome to start game press 'Play' or /start", bundle)

    print(user)
    print(client_url)
    print(bundle)

    return 'OK', 200


def send_message(chat_id, message, bundle):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == '__main__':
    # app.run()
    http_server = WSGIServer(("0.0.0.0", 5030), app)
    http_server.serve_forever()
