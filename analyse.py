from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

import credentials #file containing credentials

# To authenticate the credentials from credentials.py. Called in TwitterClient()
class Authenticate():
	def authenticate_user(self):
		auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
		auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
		return auth

#Twitter client
class TwitterClient():
	def __init__(self, twitter_user=None):
		self.auth = Authenticate().authenticate_user()
		self.twitter_client = API(self.auth)
		self.twitter_user = twitter_user

	def get_twitter_client_api(self):
		return self.twitter_client        

class Analyse():
	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def analyse_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.polarity

	def analyse_subjectivity(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.subjectivity

	def tweets_to_data_frame(self, tweets):
		df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
		df['date'] = np.array([tweet.created_at for tweet in tweets])
		df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
		df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
		return df

if __name__ == '__main__':
	twitter_client = TwitterClient()
	tweet_analyser = Analyse()
	api = twitter_client.get_twitter_client_api()
	tweets = api.user_timeline(screen_name="IAmMarkManson", count=50) #returns in JSON format
	df = tweet_analyser.tweets_to_data_frame(tweets)
	df['polarity'] = np.array([tweet_analyser.analyse_sentiment(tweet) for tweet in df['tweets']])
	df['subjectivity'] = np.array([tweet_analyser.analyse_subjectivity(tweet) for tweet in df['tweets']])
	print(df.head(50))
	# plot
	time_likes = pd.Series(data=df['likes'].values, index=df['date'])
	time_likes.plot(figsize=(16, 4), label="likes", legend=True)

	time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
	time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
	plt.show()

	time_polarity = pd.Series(data=df['polarity'].values, index=df['date'])
	time_polarity.plot(figsize=(16, 4), label="polarity", legend=True)

	time_subjectivity = pd.Series(data=df['subjectivity'].values, index=df['date'])
	time_subjectivity.plot(figsize=(16, 4), label="subjectivity", legend=True)
	plt.show()



