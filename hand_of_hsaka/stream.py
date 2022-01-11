from dotenv import dotenv_values
import tweepy
import random

config = {
  **dotenv_values("../.env")
}

class TweetListener(tweepy.Stream):
  def on_status(self, tweet):
      text = tweet.extended_tweet['full_text'] if hasattr(tweet, 'extended_tweet') else tweet.text
      print(tweet.text)

stream = TweetListener(
  config['API_KEY'], config['API_SECRET'],
  config['ACCESS_TOKEN'], config['ACCESS_TOKEN_SECRET']
)

stream.filter(follow=[config['TWITTER_USER']])
