PyJaipur Telegram Bot
=====================

A nice automated bot to keep group chats clean

Capabilities
------------

- [x] monitors chat for things that look like code and asks people to use pastebin like services
- [ ] link to previously asked questions in the chat?
- [ ] don't ask to ask just ask?


Running
=======


```bash
pipenv install --deploy
# Add your token in the correct place in the file
sudo cp pyjaipur.service /etc/systemd/system/pyjaipur.service
sudo systemctl daemon-reload
sudo service pyjaipur status
sudo service pyjaipur start
sudo service pyjaipur status
```
