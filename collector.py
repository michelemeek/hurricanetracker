#!/usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import signal


# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret will be generated for you after
consumer_key="eCKx5TBJ42FtzwkcgJM19Q"
consumer_secret="VuRYfuXX9PvzDU6EQ6PGn3DEyTnfEDOdqkSXD8G0"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="10711302-CPXQxC3pjAzl4412SKa8LdJibw2BdIBvD7B4MgtAs"
access_token_secret="vcvsx6NVkUBhyYgV1D2iT5FdQgOUiXxQqyDbz7lU"

class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream. 
	This is a basic listener that just prints received tweets to stdout.

	"""
	def on_data(self, data):
		print data
		return True

	def on_error(self, status):
		print status

class Collector(StreamListener):
	""" A listener handles tweets are the received from the stream. 
	This is a basic listener that saves the tweets in a file based on the filter.

	"""
        global output_file

        def on_data(self, data):
		output_file.write(data)
                output_file.write('\n')
		return True

	def on_error(self, status):
		print status

def SigHUPHandler(signum, frame):
        global output_file
        print "Restarting logging"
        output_file.close()
        output_file = open('collector/tweets.log', 'a')
        return

if __name__ == '__main__':
	l = Collector()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

        signal.signal(signal.SIGHUP, SigHUPHandler)

        output_file = open('collector/tweets.log', 'a')

	stream = Stream(auth, l)	
	stream.filter(track=['#hurricanesandy', '#sandy'])
