import json
import json as j

from tweepy import TweepError

from src.mongoDB.fetcher import Fetcher
from src.static.Cleaner import clearTweetJson, clearUserJson
from src.TwitterConncection import TwitterConnection
import tweepy
import pymongo


class TweetLoader:

    def __init__(self,max_comments=100,max_reply=100,restart=False):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.users = self.mydb['users']

        # TwitterConncection object
        self.api = TwitterConnection().api
        if restart:
            self.mydb.drop_collection(name_or_collection="tweets")
            self.mydb.drop_collection(name_or_collection="users")
        self.max_reply=max_reply;
        self.max_comments=max_comments


    def saveUser(self,screen_name,to_print=False):
        user=None
        try:
            user =self.api.get_user(screen_name=screen_name)
        except TweepError:
            print('No user with screen_name = '+screen_name)
        if (user == None) :
            raise Exception('No user with screen_name = '+screen_name)
        self.users.insert_one(clearUserJson(user._json))
        if (to_print):
            print("User : ")
            print(json.dumps(clearUserJson(user._json), indent=2, sort_keys=True))
            print("is saved")

    def saveTweet(self,id,to_print=False,with_author=False):
        tweet = None
        try:
            tweet = self.api.get_status(id=id)
        except Exception:
            print('No tweet with id = ' + id.__str__())
        if tweet == None:
            raise Exception('No tweet with id = ' + id.__str__())
        if tweet.__getattribute__('lang') != 'en':
            raise Exception('Tweet is not english one')
        tweet = clearTweetJson(tweet._json)
        self.tweets.insert_one(tweet)
        if (to_print):
            print("Tweet :")
            print(tweet)
            print("is saved")
        if (with_author):
            self.saveUser(screen_name=tweet['screen_name'],to_print=to_print)
        return tweet

# Saves Tweet, replies, author, and authors of replies
    def saveTweetWithAllData(self,id=-1,to_print=False,with_author=True,with_author_of_replies=False):
        tweet = self.saveTweet(id,to_print=to_print)
        self.saveUser(tweet['screen_name'],to_print=to_print)
        self.saveReplies(tweet,to_print=to_print,with_author=with_author_of_replies)

    def saveReplies(self,tweet,to_print=False,with_author=False):
        before_count =self.tweets.count()
        for reply in tweepy.Cursor(self.api.search, q='to:'+tweet['screen_name'],lang='en', since_id=tweet['id'],
                                   result_type='recent',timeout=999999).items(self.max_reply):
            self.saveTweet(reply._json['id'],to_print=to_print,with_author=with_author)
        if (to_print):
            print((self.tweets.count()-before_count).__str__()+' replies added\n')



# 1133284566632787969
if __name__ == '__main__':
    mongo=TweetLoader()
    fetch =Fetcher()
    mongo.saveTweetWithAllData(id=1133184409127989248,with_author_of_replies=True)
