from functools import wraps
from gevent.pywsgi import WSGIServer
import re
import jwt
import requests
from flask import Flask, render_template, request, jsonify

from config import *
from data.UserRepository import UserRepository

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check_db', methods=["POST"])
def chekc_db():
    request_data = request.get_json()
    if not request_data:
        print("reqest is None")
        return 'reqest is None', 400
    user = request_data.get("user", {})
    params = request_data.get("params", {})

    if not user:
        print("User not exists")
        return 'User not exists', 400

    user_id = user.get("id", None)
    username = user.get("username", None)
    first_name = user.get("first_name", None)
    language_code = user.get("language_code", None)
    client_url = params.get("client_url", None)
    bundle = params.get("bundle", None)

    print("User:", remove_non_ascii(str(user)))
    print("Client URL:", str(client_url))
    print("Bundle:", str(bundle))

    if bundle == APP1_OLYMPUS_BUNDLE:
        if not UserRepository().get_user_app1_olympus(user_id):
            if not UserRepository().add_user_app1_olympus(user_id, username, first_name, language_code, client_url):
                print("Can`t add user to bot`s table")
                return 'Can`t add user to bot`s table', 400
            else:
                send_message(user_id, "Hello, Welcome to start game press 'Play' or /start", bundle)

    elif bundle == APP2_JOKER_BUNDLE:
        if not UserRepository().get_user_app2_joker(user_id):
            if not UserRepository().add_user_app2_joker(user_id, username, first_name, language_code, client_url):
                print("Can`t add user to bot`s table")
                return 'Can`t add user to bot`s table', 400
            else:
                send_message(user_id, "Hello, Welcome to start game press 'Play' or /start", bundle)
                
    else:
        print("Bot with bundle not exists")
        return 'Bot with bundle not exists', 400

    if not UserRepository().get_user(user_id):
        if not UserRepository().add_user(user_id, username, first_name, language_code):
            print("User can`t add to all users table")
            return 'User can`t add to all users table', 400

    print("OK")
    return 'OK', 200


def send_message(chat_id, message, bundle):
    if bundle == APP1_OLYMPUS_BUNDLE:
        bot_token = BOT_TOKEN_APP1_OLYMPUS

    elif bundle == APP2_JOKER_BUNDLE:
        bot_token = BOT_TOKEN_APP2_JOKER

    else:
        print("No messaging")
        return

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    requests.post(url, data=payload)


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)


if __name__ == '__main__':
    # app.run()
    http_server = WSGIServer(("0.0.0.0", 5030), app)
    http_server.serve_forever()
