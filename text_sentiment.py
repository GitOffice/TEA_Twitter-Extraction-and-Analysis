import sys
import re
try:
	from textblob import TextBlob
except ImportError:
	print("[ERROR] Unable to import TextBlob module: can't run!")
	sys.exit()

class TweetSentiment():

	def __init__(self):
		self._status = ""

	def clean_tweet(self, tweet):
			return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		self._analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if self._analysis.sentiment.polarity > 0:
			return 'positive'
		elif self._analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'