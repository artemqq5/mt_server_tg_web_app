import json
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
    try:
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

        if bundle in BUNDLE_LIST.keys():
            if not UserRepository().get_user_transaction(user_id, bundle):
                if not UserRepository().add_user_transaction(user_id, bundle, username, first_name, language_code,
                                                             client_url):
                    print("Can`t add user to bot`s table")
                    return 'Can`t add user to bot`s table', 400
                else:
                    send_message(user_id, "Hello, Welcome to Game. Press 'Play' to Start", bundle, client_url)
        else:
            print("Bot with bundle not exists")
            return 'Bot with bundle not exists', 400

        if not UserRepository().get_user(user_id):
            if not UserRepository().add_user(user_id, username, first_name, language_code):
                print("User can`t add to all users table")
                return 'User can`t add to all users table', 400

        print("OK")
        return 'OK', 200
    except Exception as e:
        print(e)
        return 'Error', 400


def send_message(chat_id, message, bundle, client_url):
    url = f'https://api.telegram.org/bot{BUNDLE_LIST.get(bundle)}/sendMessage'
    reply_keyboard = [[{'text': 'Play', 'web_app': {'url': client_url}}]]
    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': json.dumps({
            'keyboard': reply_keyboard,
            'resize_keyboard': True,
            'one_time_keyboard': True
        })
    }

    requests.post(url, data=payload)


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)


if __name__ == '__main__':
    app.run(threaded=True)
    # http_server = WSGIServer(("0.0.0.0", 5030), app)
    # http_server.serve_forever()
