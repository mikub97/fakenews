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

    #Zapisuje użytkownika do BD
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

    #Zapisuje tweeta do BD
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

    # Zapisuje Tweet, replies, author(opcjonalnie),  authors of replies (opcjonalnie)
    def saveTweetWithAllData(self,id=-1,to_print=False,with_author=True,with_author_of_replies=False):
        tweet = self.saveTweet(id,to_print=to_print)
        self.saveUser(tweet['screen_name'],to_print=to_print)
        self.saveReplies(tweet,to_print=to_print,with_author=with_author_of_replies)

    #Zapisuje Odpowiedzi do tweeta  ------- argument tweet to FAKTYCZNIE TWEET, NIE ID
    def saveReplies(self,tweet,to_print=False,with_author=False):
        before_count =self.tweets.count()
        for reply in tweepy.Cursor(self.api.search, q='to:'+tweet['screen_name'],lang='en', since_id=tweet['id'],
                                   result_type='recent',timeout=999999).items(self.max_reply):
            self.saveTweet(reply._json['id'],to_print=to_print,with_author=with_author)
        if (to_print):
            print((self.tweets.count()-before_count).__str__()+' replies added\n')

    #Zapisuje Tweety, które są poszukując ich na zasadzie wystąpywania słów, można zaostrzyć filtrem tylko zweryfikowani autorzy
    def saveTweetsWithWords(self,words,connected_with_tweet=None,limit=1000,verified_authors_only=False,with_authors=False,to_print=False):
        cursor= tweepy.Cursor(self.api.search, q=words,lang='en',result_type='popular',timeout=999999).items(limit)
        tweets=[]
        i=0
        while True :
            if i>=limit:
                return tweets
            try:
                tweet = cursor.next()
                tweet = clearTweetJson(tweet._json,connected_with_tweet)
                user =self.api.get_user(screen_name=tweet['screen_name'])
                user = clearUserJson(user._json)
                if verified_authors_only:
                    if (user['verified']):
                        self.tweets.insert_one(tweet)
                        if (to_print):
                            print("Tweet :")
                            print(tweet)
                            print("is saved")
                        if(with_authors):
                            self.users.insert_one(user)
                            if (to_print):
                                print("User :")
                                print(user)
                                print("is saved")

                else:
                    self.tweets.insert_one(tweet)
                    if (to_print):
                        print("Tweet :")
                        print(tweet)
                        print("is saved")
                    if (with_authors):
                        self.users.insert_one(user)
                        if (to_print):
                            print("User :")
                            print(user)
                            print("is saved")
                i=i+1
            except StopIteration :
                return
            
    #Zapisuje autora Tweetu
    def saveAuthor(self,id):
        tweet =self.api.get_status(id=id)
        self.users.insert_one(clearUserJson(self.api.get_user(screen_name=tweet.author.screen_name)))


# 1133284566632787969
if __name__ == '__main__':

    mongo=TweetLoader(restart=True)
    #Pobieranie konkretnego tweeta, bez autora
    mongo.saveTweet(id=1133184409127989248,to_print=True,with_author=False)

    # Pobieranie konkretnego użytkonika
    mongo.saveUser(screen_name='potus',to_print=True)
    # Pobieranie konkretnego tweetu, jego autora, odpowiedziami do tweetu i ich autorami
    # mongo.saveTweetWithAllData(id=1133184409127989248,with_author_of_replies=True,to_print=True)

    #Działanie pobierania tweetów powiązanych
    mongo.saveTweetsWithWords(['Oklahoma','Japan'],connected_with_tweet='z tym ID',limit=100,verified_authors_only=True,to_print=True,with_authors=True)