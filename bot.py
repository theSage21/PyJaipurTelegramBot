import shelve
import argparse
import requests
import logging
from telegram.ext import Updater, MessageHandler, Filters


parser = argparse.ArgumentParser()
parser.add_argument('token', help='Bot token')
parser.add_argument('--shelf', default='shelf', help='Where to store shelf data')
parser.add_argument('-n_code_lines_ok', default=10, help='How many lines of code like stuff is acceptable?')
parser.add_argument('-ignore_n_offences', default=3, help='How many offences to ignore before reminding a person?')
args = parser.parse_args()

updater = Updater(args.token)
unnatural_chars = ['=', '==', '(', ')', '[', ']', ';', '<', '>', '{', '}']
# ===============================
def is_code(text):
    lines = (i for i in text.split('\n') if i.strip() != '')
    code_lines = [line for line in lines if any([char in line for char in unnatural_chars])]
    return len(code_lines) > args.n_code_lines_ok


def paste(message):
    r = requests.post('https://dpaste.de/api/', data={'content': message, 'format': 'url'})
    return r.text


def echo(bot, update):
    if is_code(update.message.text):
        with shelve.open(args.shelf) as known_offenders:
            uid = str(update.message.from_user.id )
            offences = known_offenders.get(uid, {'offence_count': 0, 'last_warning_at_count': 0})
            offences['offence_count'] += 1
            known_offenders[uid] = offences
        if (offences['offence_count'] - offences['last_warning_at_count']) % args.ignore_n_offences != 0:
            link = paste(update.message.text)
            msg = f"Please use a paste service: { link }"
        update.message.reply_text(msg)



updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()
