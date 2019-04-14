import shelve
import argparse
import requests
import logging
from telegram.ext import Updater, MessageHandler, Filters


parser = argparse.ArgumentParser()
parser.add_argument('token', help='Bot token')
parser.add_argument('--shelf', default='shelf', help='Where to store shelf data')
args = parser.parse_args()

updater = Updater(args.token)
unnatural_chars = ['=', '==', '(', ')', '[', ']', ';', '<', '>', '{', '}']
# ===============================
def is_code(text):
    lines = (i for i in text.split('\n') if i.strip() != '')
    code_lines = [line for line in lines if any([char in line for char in unnatural_chars])]
    return len(code_lines) > 1


def paste(message):
    r = requests.post('https://dpaste.de/api/', data={'content': message, 'format': 'url'})
    return r.text


def echo(bot, update):
    if is_code(update.message.text):
        link = paste(update.message.text)
        with shelve.open(args.shelf) as known_offenders:
            uid = str(update.message.from_user.id )
            serial_offender = uid in known_offenders
            if not serial_offender:
                known_offenders[uid] = True
        if serial_offender:
            msg = f"Please use a paste service: { link }"
        else:
            msg = f'''Looks like you just pasted some code in the chat. This makes the chat unreadable. I've pasted your message for you this time:

            { link }

            In the future use one of these services:

            - dpaste.de
            - pastebin.com
            - gist.github.com
            '''
        update.message.reply_text(msg)



updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()
