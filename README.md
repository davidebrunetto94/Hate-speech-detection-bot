# Hate-speech-detection-bot
A Telegram bot that uses a SVM classifier to tell whether a certain topic or a certain user's timeline contains hate speech.
The project is composed of 4 main modules:

 * **tweets.py**, this module handles the authentication to the Twitter API and the retrieval of the tweets.
 * **pp.py**, this module handles all of the preprocessing of the tweets. The main function is "cleanTweets" that takes in input raw tweets and, using some helper functions based on regex, processes them to make them more suitable for the classification.
* **classification.py**, this module handles the classification of the tweets using a precomputed svm model
 * **bot.py**, this module handles the tasks related to the bot messages and replies. It filters the messages that it receives using regexs and sends the correct replies.
 
 To utilize this project the constants declared in **secrets.py** need to be replaced with the actual ones, obtained from the [Twitter Developer Portal](https://developer.twitter.com/en)
 
 
 The creation of the SVM model and the tf-idf vectorizer used in the project with their respective classification reports can be found [here](https://colab.research.google.com/drive/1MX-40hylAMEqLjpaAB-CuqSKyKIzmvlA?usp=sharing), along with other tries using different classifiers and word embedding methods.
