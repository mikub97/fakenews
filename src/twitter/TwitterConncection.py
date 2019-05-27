import datetime
import json
import os
import re

import tweepy
from textblob import TextBlob


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

    # Check if tweet is published by bot by:
    #   if the tweet is retweeted -> not bot
    #   if user have not ever published 10 tweets -> bot
    #   if time between respective tweets is greater than 2 days -> bot
    def isBot(self, tweet):
        if tweet.retweet_count > 0:
            return False
        else:
            user_name = tweet.user.screen_name
            last_tweets = self.api.user_timeline(screen_name=user_name, count=10, tweet_mode='extended')
            if len(last_tweets) < 10:
                return True
            else:
                for idx, tweet in enumerate(last_tweets):
                    if idx > 0:
                        current_tweet_date = last_tweets[idx].created_at
                        tweet_date = last_tweets[idx-1].created_at
                        two_days = datetime.timedelta(days=2)
                        if (tweet_date - current_tweet_date) > two_days:
                            return True
            return False

    def getTweets(self, query, count=20):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)

            for tweet in fetched_tweets:
                username = tweet.user.screen_name
                parsed_tweet = {'username': tweet.user.screen_name,
                                'retweets': tweet.retweet_count,
                                'isBot': self.isBot(tweet),
                                'text': tweet.text,
                                'sentiment': self.getTweetSentiment(tweet),
                                }
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

    def proba(self):
        print("------------------")

        elo = self.api.user_timeline(screen_name="mamastarlight")
        siema = [tweet for tweet in elo]
        for tweet in siema:
            print(tweet)

        print("------------------")


def main():
    # TwitterConncection object
    api = TwitterConnection()

    api.proba()

    # Count specifies max number of results for mentioning "Donald Trump"
    tweets = api.getTweets(query="Donald Trump", count=100)

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
