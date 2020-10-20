import re
import unicodedata
import nltk
from nltk.tokenize import TweetTokenizer

tweet_tokenizer = TweetTokenizer()
ita_stemmer = nltk.stem.snowball.ItalianStemmer()


# Function to remove URLS from the tweets
def removeUrls(tweet):
    pattern = r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"
    return re.sub(pattern, "", tweet)


# Function to remove the mentions of users from the tweet
def removeAt(tweet):
    pattern = r"@\w*"
    return re.sub(pattern, "", tweet)


# Function to remove repeated letters
def removeRepetitions(tweet):
    pattern = r"(.)\1{2,}"
    return re.sub(pattern, r"\1", tweet)


# Function to remove RT|FAV words that are in raw tweets
def removeReservedWords(tweet):
    pattern = r"^(RT|FAV)"
    return re.sub(pattern, "", tweet)


# Function to remove digits
def removeDigitsv2(tweet):
    return "".join([i for i in tweet if not i.isdigit()])


# Function to remove emojis
def removeEmojis(tweet):
    emojiPattern = re.compile(
        pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return emojiPattern.sub("", tweet)


# Function to remove smileys
def removeSmileys(tweet):
    smileysPattern = re.compile(
        r"(\s?:X|:|;|=)(?:-)?(?:\)+|\(|O|D|P|S|\\|\/\s){1,}", re.IGNORECASE
    )
    return smileysPattern.sub("", tweet)


# Function to remove punctuation
def removePunctuation(tweet):
    noSpacePattern = re.compile(
        r'(\.+)|(\«)|(\»)|(\;)|(\:)|(\!)|(\?)|(\,)|(")|(\“)|(\”)|(\’)|(\|)|(\()|(\))|(\[)|(\])|(\%)|(\$)|(\>)|(\<)|(\{)|(\})'
    )
    withSpacePattern = re.compile(r"(<br\s/><br\s/?)|(-)|(/)|(')|(:).")
    preCleanTweet = noSpacePattern.sub(" ", tweet)
    return withSpacePattern.sub(" ", preCleanTweet)


# This function only removes the # symbol before the word, not the entire word
def removeHashtags(tweet):
    return tweet.replace("#", " ")


# Removes characters that are not ascii
def removeNonAscii(tweet):
    encoded_string = tweet.encode("ascii", "ignore")
    return encoded_string.decode()


def unicodeNormalize(tweet):
    return unicodedata.normalize("NFKD", tweet)


# Snowball stemmer with rules for the Italian language
def italianStemmer(tweet):
    return [ita_stemmer.stem(word) for word in tweet]


def cleanTweets(df):
    cleanTweetsList = []
    for tweet in df:
        # tweet = removeUrls(tweet) #not useful with this ds
        tweet = unicodeNormalize(tweet)
        tweet = removeUrls(tweet)
        # tweet = removeUrls(tweet)
        tweet = removeAt(tweet)
        tweet = removePunctuation(tweet)
        tweet = removeReservedWords(tweet)
        tweet = removeSmileys(tweet)
        tweet = removeHashtags(tweet)
        tweet = removeEmojis(tweet)
        tweet = removeDigitsv2(tweet)
        tweet = removeRepetitions(tweet)
        tweet = tweet_tokenizer.tokenize(tweet)
        tweet = italianStemmer(tweet)
        tweet = " ".join(tweet)
        # tweet = removeNonAscii(tweet) #not useful with italian ds
        cleanTweetsList.append(tweet)
    return cleanTweetsList
