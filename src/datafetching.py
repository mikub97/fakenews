import re

from src.mongo import clearTweetJson
from src.twitter.TwitterConncection import TwitterConnection
import tweepy
import pymongo
from textblob import TextBlob
import json

class DataFetching():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.comments = self.mydb['comments']




    def print_tweets(self):
        print(self.tweets.count().__str__() + ' objects in the DB')
        for x in self.tweets.find():
            clearTweetJson(x)
            print(json.dumps(x, indent=2, sort_keys=True))
            print('\n')


if __name__ == '__main__':
    fetch = DataFetching()
    fetch.print_tweets()
