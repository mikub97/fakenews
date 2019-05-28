import re

import pymongo

class Fetcher():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.users = self.mydb['users']

    def get_tweet(self,id):
        return self.tweets.find_one({'id':id})


    def get_user(self,screen_name):
        return self.users.find_one({'screen_name':screen_name})

    def get_author_of_tweet(self,id):
        tweet = self.get_tweet(id)
        return self.users.find_one({'screen_name':tweet['screen_name']})

    def get_replies(self, id):
        return self.tweets.find({'in_reply_to_status_id':id})

    def print_stats(self):
        print("There are " + self.users.count().__str__() + " users in db")
        print("There are " + self.tweets.count().__str__() + " tweets in db")

    def print_tweets(self):
        i=1
        print("TWEETS:")
        for x in self.tweets.find():
            print(i.__str__()+".")
            print(x)
            print('\n')
            i=i+1
    def print_users(self):
        i=1
        print("USERS:")
        for x in self.users.find():
            print(i.__str__()+".")
            print(x)
            print('\n')
            i=i+1

if __name__ == '__main__':
    fetch = Fetcher()
    fetch.print_stats()
