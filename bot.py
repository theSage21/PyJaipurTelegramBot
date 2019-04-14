import shelve
import argparse
import requests
from telegram.ext import Updater, MessageHandler, Filters


parser = argparse.ArgumentParser()
parser.add_argument('token', help='Bot token')
args = parser.parse_args()

updater = Updater(args.token)
unnatural_chars = ['=', '==', '(', ')', '[', ']', ':', ';', '<', '>', '{', '}']
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
        print('looks like code')
        link = paste(update.message.text)
        with shelve.open(shelf) as shelf:
            first_mistake = shelf.get(update.message.from_user.id) is None
            if first_mistake:
                shelf[update.message.from_user.id] = True
        if not first_mistake:
            msg = f'Please use a paste service: { link }'
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
