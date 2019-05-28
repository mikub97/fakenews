import datetime

import requests
from textblob import TextBlob

from TwitterConncection import TwitterConnection
from twitter.UrlMachineLearner import UrlMachineLearner


class BotChecker:

    def __init__(self):
        self.api = TwitterConnection().api

    def getTweetSentiment(self, tweet):
        analysis = TextBlob(tweet.full_text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'

    #   Checking if tweet is fake based on frequency of posting the tweets
    def isBot(self, tweet):
        if tweet.retweet_count > 0:
            return False
        else:
            user_name = tweet.user.screen_name
            last_tweets = self.api.user_timeline(screen_name=user_name, count=10, tweet_mode='extended',
                                                 include_entities=True)
            if len(last_tweets) < 10:
                return True
            else:
                for idx, tweet in enumerate(last_tweets):
                    if idx > 0:
                        current_tweet_date = last_tweets[idx].created_at
                        tweet_date = last_tweets[idx - 1].created_at
                        two_days = datetime.timedelta(days=2)
                        if (tweet_date - current_tweet_date) > two_days:
                            return True
            return False

    # Checking if tweet is fake based on external urls provided in a tweet
    def is_fake_external_urls(self, tweet, useMachineLearning):
        urls = tweet.entities['urls']
        if len(urls) <= 0:
            return False
        for url in urls:
            full_url = url['expanded_url']
            if not useMachineLearning:
                try:
                    headers = requests.utils.default_headers()
                    headers.update(
                        {
                            'User-Agent': 'My User Agent 1.0',
                        }
                    )
                    response = requests.get(full_url, headers=headers)
                    http_code = response.status_code
                    if (http_code / 100) >= 4:
                        return True
                except:
                    print('Site does not let us in, conisdering tweet as fake')
                    return True

                return False
            else:
                data_machine_learner = UrlMachineLearner()
                return data_machine_learner.is_url_malicious(full_url)

    def parse_tweet(self, tweet, machineLearning):
        parsed_tweet = {'username': tweet.user.screen_name,
                        'retweets': tweet.retweet_count,
                        'isBot': self.isBot(tweet),
                        'isFakeBasedOnExternalUrl': self.is_fake_external_urls(tweet,
                                                                               useMachineLearning=machineLearning),
                        'full_text': tweet.full_text,
                        'sentiment': self.getTweetSentiment(tweet),
                        }
        return parsed_tweet

    def is_fake_based_on_user(self, tweet):
        parsed_tweet = self.parse_tweet(tweet, True)
        return parsed_tweet['isBot']

    def is_fake_based_on_external_urls(self, tweet):
        parsed_tweet = self.parse_tweet(tweet, True)
        return parsed_tweet['isFakeBasedOnExternalUrl']

    def get_tweet_sentiment(self, tweet):
        parsed_tweet = self.parse_tweet(tweet)
        return parsed_tweet['sentiment']

    # Determine is tweet is fake based on frequency of posted tweets by user and on external urls in tweets if
    # machineLearning == true than program will check the urls in tweets based on machine learning - not very
    # accurate
    # if not machineLearning porgram will check the HTTP status to the external urls - accurate but not
    # checking if url is malicious
    def is_fake(self, tweet, isMachineLearnignOn):
        if isMachineLearnignOn:
            parsed_tweet = self.parse_tweet(tweet, True)
            return parsed_tweet['isBot'] or parsed_tweet['isFakeBasedOnExternalUrl']
        else:
            parsed_tweet = self.parse_tweet(tweet, False)
            return parsed_tweet['isBot'] or parsed_tweet['isFakeBasedOnExternalUrl']


#Sample invoke
def main():
    obj = BotChecker()
    tweets = obj.api.search(q="Donald Trump", tweet_mode='extended', count=100, include_entities=True)
    for tweet in tweets:
        print('is fake based on user: ', obj.is_fake_based_on_user(tweet))
        print('is fake based on external urls: ', obj.is_fake_external_urls(tweet))


#Sample invoke
if __name__ == '__main__':
    main()
