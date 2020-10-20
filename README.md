# Hate-speech-detection-bot
A Telegram bot that uses a SVM classifier to tell whether a certain topic or a certain user's timeline contains hate speech.
The project is composed of 4 modules:

 * **tweets.py**, this module handles the authentication to the Twitter API and the retrieval of the tweets.
 * **pp.py**, this module handles all of the preprocessing of the tweets. The main function is "cleanTweets" that takes in input raw tweets and, using some helper functions based on regex, processes them to make them more suitable for the classification.
* **classification.py**, this module handles the classification of the tweets using a precomputed svm model
 * **bot.py**, this module handles the tasks related to the bot messages and replies. It filters the messages that it receives using regexs and sends the correct replies.
