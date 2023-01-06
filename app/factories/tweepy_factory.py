import os
import tweepy

def create_instance() -> tweepy.Client:
  """
  Create instance of a tweepy twitter API v2 client.
  """
  client = tweepy.Client(bearer_token=os.environ['TWITTER_BEARER_TOKEN'])
  return client
