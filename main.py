import os
import sys
import tweepy
from textblob import TextBlob
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()
bearer_token = os.environ.get("BEARER_TOKEN")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Tweepyの認証
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

# コマンドライン引数から検索するキーワードを取得
if len(sys.argv) > 1:
    search_query = sys.argv[1]
else:
    print("Usage: python script.py <search_keyword>")
    sys.exit(1)

# ツイートの感情分析
def analyze_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    return analysis.sentiment.polarity

# 指定したキーワードで検索し、ツイートがネガティブな場合にユーザーをブロック
# [TODO] 無料版をためしたので実際に動くかわからない、おそらくブロックする時にIDを指定しないといけない
def block_negative_users():
    try:
        tweets = client.search_recent_tweets(
            query=search_query,
            max_results=100
        )
        for tweet in tweets:
            tweet_text = tweet.text
            sentiment_score = analyze_sentiment(tweet_text)

            if sentiment_score < 0:
                user_to_block = tweet.user.screen_name
                client.block(target_user_id=user_to_block)
                print(f"Blocked user: {user_to_block} - Tweet: {tweet_text}")
    except tweepy.TweepyException as e:
        print(f"An error occurred during the search: {str(e)}")

if __name__ == "__main__":
    block_negative_users()
