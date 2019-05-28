import json as j

from src.static.Cleaner import clearTweetJson
from src.TwitterConncection import TwitterConnection
import tweepy
import pymongo


class TweetLoader:

    def __init__(self,max_comments=100,max_reply=100):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.comments = self.mydb['comments']
        # TwitterConncection object
        self.api = TwitterConnection().api
        self.mydb.drop_collection(name_or_collection="tweets")
        self.mydb.drop_collection(name_or_collection="comments")
        self.max_reply=max_reply;
        self.max_comments=max_comments

    def saveTweetWithDataById(self,id=-1):
        tweet = None
        if (id==-1):
            search = self.api.user_timeline(screen_name='realDonaldTrump', count=1)
            tweet = search[0]
        else :
            tweet = self.api.get_status(id=id)
        if tweet == None:
            raise Exception('No tweet with id = ' +id.__str__())
        if tweet.__getattribute__('lang') != 'en':
            raise Exception('Tweet is not english one')
        before_count =self.tweets.count()
        json = tweet._json
        self.tweets.insert_one(clearTweetJson(json))
        print((self.tweets.count()-before_count).__str__()+' tweets added\n')
        clearTweetJson(json)
        print(j.dumps(json, indent=2, sort_keys=True))
        self.saveReplies(tweet)

    def saveReplies(self,tweet):
        before_count =self.tweets.count()
        for tweet in tweepy.Cursor(self.api.search, q='to:'+tweet.author.screen_name,lang='en', since_id=tweet.id,
                                   result_type='recent',timeout=999999).items(self.max_reply):
            json = tweet._json
            json = clearTweetJson(json)
            self.tweets.insert_one(json)
        print((self.tweets.count()-before_count).__str__()+' replies added\n')



# 1133284566632787969
if __name__ == '__main__':
    mongo=TweetLoader()
    mongo.saveTweetWithDataById(id=1133284566632787969)
