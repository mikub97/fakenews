import re
from src.twitter.TwitterConncection import TwitterConnection
import tweepy
import pymongo
from textblob import TextBlob
import json

class dataFetching():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.mycol = self.mydb["tweets"]



def main():
    mongo = dataFetching()
    for x in mongo.mycol.find():
        id = x['id']
        text = x['text']
        sentiment = x['sentiment']
        friendsCount = x['friendsCount']
        followersCount = x['followersCount']
        comments = x['comments']
        retweetCount = x['retweetCount']
        username = x['username']
        date = x['date']
        #tu podpinamy kolejne moduły
        #np.
        #ml = MachineLearningModule()
        #wynik_machine_learning = ml.machine_eval(text,id)
        print(id, text, sentiment, friendsCount, followersCount, comments, retweetCount, username, date)


if __name__ == '__main__':
    main()
