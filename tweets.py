import tweepy
from typing import List
from datetime import datetime, timedelta
from secrets import CONS_KEY, CONS_SECRET, ACC_SECRET, ACC_TOKEN

# Function to authenticate to the Twitter API
def authentication(cons_key, cons_secret, acc_token, acc_secret):
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    api = tweepy.API(auth)
    return api


# Function to get the last 10 tweets for a specific keyword
def get_tweets_by_keyword(keyword: str) -> List[str]:
    all_tweets = []
    api = authentication(CONS_KEY, CONS_SECRET, ACC_TOKEN, ACC_SECRET)
    yesterday_datetime = datetime.today().now() - timedelta(days=1)
    yesterday_date = yesterday_datetime.strftime("%Y-%m-%d")
    try:
        for tweet in tweepy.Cursor(
            api.search,
            q=keyword,
            tweet_mode="extended",
            since=yesterday_date,
            result_type="recent",
            lang="it",
        ).items(10):
            all_tweets.append(tweet.full_text)
    except Exception:
        print("Topic not found")
    return all_tweets


# Function to get the last 10 tweets by a specific user
def get_tweets_by_user(screen_name: str) -> List[str]:
    all_tweets = []
    api = authentication(CONS_KEY, CONS_SECRET, ACC_TOKEN, ACC_SECRET)
    screen_name = "@" + screen_name
    try:
        for tweet in tweepy.Cursor(
            api.user_timeline, screen_name=screen_name, tweet_mode="extended"
        ).items(10):
            all_tweets.append(tweet.full_text)
    except Exception:
        print("User not found")
    return all_tweets


# def clean_tweets(all_tweets: List[str]) -> List[str]:
#     tweets_clean = []
#     for tweet in all_tweets:
#         #remove usernames
#         user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet)
#         #remove links
#         link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
#         #remove numbers
#         number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
#         #make the tweet lowercase
#         lower_case_tweet= number_removed.lower()
#         #remove unnecessary spaces
#         tok = WordPunctTokenizer()
#         words = tok.tokenize(lower_case_tweet)
#         clean_tweet = (' '.join(words)).strip()
#         print("Clean tweet ")
#         print(clean_tweet)
#         print("\n")
#         print("Original tweet ")
#         print(tweet)
#         tweets_clean.append(clean_tweet)
#     return tweets_clean

# def get_sentiment(all_tweets: List[str]) -> List[float]:
#     sentiment_scores = []
#     for tweet in all_tweets:
#         blob = TextBlob(tweet)
#         sentiment_scores.append(blob.sentiment.polarity)
#     return sentiment_scores

# def generate_average_sentiment_score(keyword: str) -> int:
#     tweets = get_tweets(keyword)
#     tweets_clean =clean_tweets(tweets)
#     sentiment_scores = get_sentiment(tweets_clean)
#     average_score = statistics.mean(sentiment_scores)
#     return average_score

# if __name__ == "__main__":
#     print("What does the world prefer?")
#     first_input = input()
#     print('...or...')
#     second_input = input()
#     print("\n")

#     first_score = generate_average_sentiment_score(first_input)
#     second_score = generate_average_sentiment_score(second_input)

#     print(f"The first score is {first_score} and the second score is {second_score}")
#     if(first_score > second_score):
#         print(f"The humanity prefers {first_input} over {second_input}")
#     elif(first_score < second_score):
#         print(f"The humanity prefers {second_input} over {first_input}")
#     else:
#         print("The two are equal")
