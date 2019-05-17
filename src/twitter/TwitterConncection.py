import json

import tweepy


class TwitterConnection:

    def connect(self):
        # Load credentials
        with open("twitter-credentials.json") as file:
            credentials = json.load(file)

        auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
        auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

        return tweepy.API(auth)


if __name__ == '__main__':
    connection = TwitterConnection()
    api = connection.connect()

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    # get user object for twitter
    user = api.get_user('twitter')
    print(user.screen_name)
    print(user.followers_count)
    for friends in user.friends():
        print(friends.screen_name)
