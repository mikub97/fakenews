import json
import _pickle as pickle
import os
import re
from textblob import TextBlob

import tweepy


class TwitterConnection:

    def __init__(self):
        # Load credentials
        with open("twitter-credentials.json") as file:
            credentials = json.load(file)
        try:
            self.auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
            self.auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication failed")

    # Sample:
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                               "|(\w+:\/\/\S+)",
                               " ",
                               tweet).split())

    def getTweetSentiment(self, tweet):
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'

    def getTweets(self, query, count=20):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)

            for tweet in fetched_tweets:
                parsed_tweet = {'text': tweet.text, 'sentiment': self.getTweetSentiment(tweet)}
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error: " + str(e))


def main():
    # TwitterConncection object
    api = TwitterConnection()

    # Count specifies max number of results
    tweets = api.getTweets(query="Donald Trump", count=10)

    # Picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # Percentage of positive tweets
    print("Positive tweets percentage: {}%".format(100 * len(ptweets) / len(tweets)))
    # Picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # Percentage of them
    print("Negative tweets percentage: {}%".format(100 * len(ntweets) / len(tweets)))

    # Printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    # Printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # saving tweets to .json files in 'tweets' directory:
    path = os.path.dirname(__file__)
    path += "/tweets"
    if not os.path.exists(path):
        os.makedirs(path)
    for idx, tweet in enumerate(tweets):
        with open(os.path.join(path, 'tweet{}.json'.format(idx)), 'w') as output:
            output.write(json.dumps(tweet))


if __name__ == '__main__':
    main()
