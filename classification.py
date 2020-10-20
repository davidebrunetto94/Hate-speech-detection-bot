import sklearn
from sklearn import svm
from joblib import load, dump
import pp as preprocessing
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

nltk.download("stopwords")


def predict_hate_speech_tweets(tweets_list):
    svm = load("svm.joblib")
    vectorizer = load("vectorizer.joblib")
    # Preprocessing of the tweets
    clean_tweets = preprocessing.cleanTweets(tweets_list)

    # Vectorization of the tweets
    X = vectorizer.transform(clean_tweets)

    # Prediction
    tweets_prediction = svm.predict(X)
    for pred, tweetClean, tweet in zip(tweets_prediction, clean_tweets, tweets_list):
        if pred == 1:
            print(f"Tweet considerato hate speech {tweet}")
    return np.sum(tweets_prediction > 0)