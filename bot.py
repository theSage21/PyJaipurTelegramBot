import argparse
import requests
from telegram.ext import Updater, MessageHandler, Filters


parser = argparse.ArgumentParser()
parser.add_argument('token', help='Bot token')
args = parser.parse_args()

updater = Updater(args.token)
# ===============================
def is_code(text):
    lines = [i for i in text.split('\n') if i.strip() != '']
    if len(lines) > 1:
        unnatural_chars = ['=', '==', '(', ')', '[', ']', ':', ';']
        if any(char in text for char in unnatural_chars):
            return True
    return False


def paste(message):
    r = requests.post('https://dpaste.de/api/', data={'content': message, 'format': 'url'})
    return r.text


def echo(bot, update):
    if is_code(update.message.text):
        print('looks like code')
        link = paste(update.message.text)
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
