# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import sys
import yamlsettings

from telebot import TeleBot
from transbotor.translations import languages, translate
from transbotor.brain import db, User, get_user

app = TeleBot(__name__)


@app.route('/register ?(.*)')
def register_lang(message, request):
    request_user = message['from']['id']

    print("{} requesting registration".format(request_user))

    send = None
    if request not in languages:
        send = "Invalid language ({}) must be formatted as ISO 639-1".format(
            request
        )
    elif get_user(request_user) is None:
        for x in User.select().where(User.admin == True):
            app.send_message(
                x,
                "Translation Request for:\n"
                "   {} - {} {} ({})\n"
                "With:\n"
                "   {}".format(message['from'].get('username', "?"),
                               message['from'].get('first_name', "???"),
                               message['from'].get('last_name', "???"),
                               request_user,
                               request),
            )
        send = "Request has been sent to the admins."
    else:
        send = "With a DB I would 'o changed your language to {}".format(
            request
        )

    app.send_message(request_user, send)


@app.route('/translate(.*)')
def demo_translation(message, captured):
    print("Demo Translation Request")

    app.send_message(
        message['chat']['id'],
        "YELLING IS A TRANSLATION {}".format(captured.upper()),
    )


@app.route('(?!/).+')
def translate_msg(message):
    print(message)

    if 'text' not in message:
        print("Non Text Message")
        return

    request_user = message['from']['id']
    request_dest = message['chat']['id']
    request_text = message['text']
    request_pair = get_user(request_user).langpair

    # Don't pay attention to the bot.
    if request_user == app.whoami['id']:
        return
    # Need to figure out how to register someone that's
    # bilingual (dual translation?)
    elif request_pair == "__|__":
        print("User is bilingual")
        return

    try:
        print(
            "Attempting to translate: {} for {} "
            "with {} to {}"
            .format(request_text, request_user,
                    request_pair, request_dest)
        )

        w = app.send_message(
            request_dest,
            translate(request_text, request_pair, request_user),
        )
        print(w)

    except Exception as e:
        print("No Translation")
        print(e)


def run():
    try:
        db.connect()
        load_error = None
        try:
            settings = yamlsettings.load('settings.yaml')
            if "api_key" not in settings:
                load_error = "Invalid settings.yaml"
        except OSError:
            load_error = "Unable to find settings.yaml"

        if load_error:
            print("Error: {}".format(load_error))
            print("Example settings.yaml:\n  ---\n  api_key: 'telegram:key'\n")
            sys.exit(1)

        app.config['api_key'] = settings.api_key
        app.poll(debug=False)
    finally:
        db.close()
