import re

from src.static.Cleaner import clearTweetJson
import pymongo
import json

class Fetcher():
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
    fetch = Fetcher()
    fetch.print_tweets()
