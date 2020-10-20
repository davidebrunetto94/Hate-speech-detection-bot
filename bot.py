#!/usr/bin/env python

import tweets as tw
import pp as preprocessing
import logging
import classification as cl
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi, this is a bot that can detect if a Twitter user's feed"
        + ' or a certain topic contains hate speech. To start send "@" followed by a twitter username'
        + 'or "#" followed by a topic!'
    )


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "This is a bot that can detect if a Twitter user's feed"
        + "or a certain topic contains hate speech!"
    )


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def user_hate_speech(update, context):
    username = update.message.text
    update.message.reply_text(f"Checking if {username} is using hate speech...")
    tweets = tw.get_tweets_by_user(username.replace("@", ""))
    if not tweets:
        update.message.reply_text("I haven't found any tweet for that user, try again")
    else:
        hate_speech_present = cl.predict_hate_speech_tweets(tweets)
        if hate_speech_present:
            update.message.reply_text("I think the user is using hate speech")
        else:
            update.message.reply_text("I don't think the user is using hate speech")


def topic_hate_speech(update, context):
    topic = update.message.text
    update.message.reply_text(f"Checking if {topic} contains hate speech...")
    tweets = tw.get_tweets_by_keyword(topic.replace("#", ""))
    if not tweets:
        update.message.reply_text("I haven't found any tweet for that topic, try again")
    else:
        hate_speech_present = cl.predict_hate_speech_tweets(tweets)
        if hate_speech_present:
            update.message.reply_text("I think that topic contains hate speech")
        else:
            update.message.reply_text(
                "I don't think that the topic contains hate speech"
            )


def incorrect_message(update, context):
    update.message.reply_text(
        "The message you typed is incorrect "
        + 'To try again, send "@" followed by a twitter username'
        + 'or "#" followed by a topic!'
    )


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TELETOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.regex(r"^[@][\w]+"), user_hate_speech))
    dp.add_handler(MessageHandler(Filters.regex(r"^[#][\w]+"), topic_hate_speech))
    dp.add_handler(MessageHandler(Filters.text, incorrect_message))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()