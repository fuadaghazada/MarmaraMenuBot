'''
    Basic bot functions

    @author: Fuad Aghazada
'''
import json
import requests
import urllib
import re
import time

import config

# API of the Currency Bot
TOKEN = config.BOT_TOKEN

# URL for accesing the API
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Access the URL and catch the content of the URL in UTF-8
# @param: url - given url
# @return: content - content of the url

def getURL(url):

    response = requests.get(url)
    content = response.content.decode("utf8")

    return content


# Loads the content of the given url in JSON format
# @param: url - given url
# @return: js - content in JSON format

def getJSON(url):

    content = getURL(url)
    js = json.loads(content)

    return js


# Acesses the updates in the API according to the given offset
# @param: (default None) - given offset
# @return: js - updates in JSON format

def getUpdates(offset = None):

    url = URL + "getUpdates?timeout=100"

    if offset:
        url += "&offset={}".format(offset)
    js = getJSON(url)

    return js


# For sending Message from Bot API
# @param: text - content of message
# @param: chat_id - ID for the receiver chat
# @param: reply_markup - for creating custom keyboard

def sendMessage(text, chat_id, reply_markup = None):

    text = urllib.parse.quote_plus(text)    # for parsing special chars like + - & etc.

    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)

    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)

    getURL(url)


# Returns the latest update ID
# @param: updates - all the updates
# @return: max of the update ids

def getLastUpdateID(updates):

    update_ids = []

    for update in updates["result"]:

        update_ids.append(int(update["update_id"]))

    return max(update_ids)


# Requests location of the user
# @param chat_id: chat id of the user

def requestLocation(chat_id):

    reply_markup = createKeyboard(["Send me your location"], location = True)

    sendMessage("Can you share your location with me?", chat_id, reply_markup)


# Updating process

def update(updates, func):

    for update in updates["result"]:

        chat = update["message"]["chat"]["id"]

        if "text" in update["message"]:
            text = update["message"]["text"]

            func(text, chat)


# Updates the processes on foreground

def update_bot(func):

    last_update_id = None

    while True:
        updates = getUpdates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = getLastUpdateID(updates) + 1
            update(updates, func)

        time.sleep(0.5)
