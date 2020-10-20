import json
import urllib3
from urllib.parse import urlparse
import pp as preprocessing
import tweets as tw
import classification as cc

TELE_TOKEN = "xxxxxxxxxxxxxxxxx"
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)


def send_message(text, chat_id):
    http = urllib3.PoolManager()
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    response = http.request("POST", url, retries=False)


def lambda_handler(event, context):
    message = json.loads(event["body"])
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]

    if text[0] == "@":
        userName = text.replace("@", "")
        send_message("checking...", chat_id)
        tweets = tw.get_tweets_by_user(userName)
        # reply = userName
    elif text[0] == "#":
        topic = text.replace("#", "")
        send_message("checking...", chat_id)
        tweets = tw.get_tweets_by_keyword(topic)
        # reply = topic
    else:
        reply = "The message was not correct. Please try again"

    hate_speech = cc.predict_hate_speech_tweets(tweets)

    if hate_speech:
        reply = "I found hate speech in the tweets"
    else:
        reply = "I haven't found any hate speech in the tweets"
    send_message(reply, chat_id)
    return {"statusCode": 200}
