import json
import json as j

from tweepy import TweepError

from src.mongoDB.fetcher import Fetcher
from src.static import Cleaner
from src.static.Cleaner import clearTweetJson, clearUserJson
from src.TwitterConncection import TwitterConnection
import tweepy
import pymongo


class TweetLoader:

    def __init__(self, max_reply=1000, restart=True):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.users = self.mydb['users']

        # TwitterConncection object
        self.api = TwitterConnection().api
        if restart:
            self.mydb.drop_collection(name_or_collection="tweets")
            self.mydb.drop_collection(name_or_collection="users")
        self.max_reply = max_reply

    # Zapisuje użytkownika do BD
    def saveUser(self, screen_name, to_print=False):
        user = None
        try:
            user = self.api.get_user(screen_name=screen_name)
        except TweepError:
            print('No user with screen_name = ' + screen_name)
        if (user == None):
            raise Exception('No user with screen_name = ' + screen_name)
        self.users.insert_one(clearUserJson(user._json))
        if (to_print):
            print("User : ")
            print(json.dumps(clearUserJson(user._json), indent=2, sort_keys=True))
            print("is saved")

    # Zapisuje tweeta do BD
    def saveTweet(self, id, to_print=False, with_author=False):
        if (self.tweets.find_one({'id': id}) != None):
            return
        tweet = None
        try:
            tweet = self.api.get_status(id=id, tweet_mode='extended')
        except Exception:
            print('No tweet with id = ' + id.__str__())
        if tweet == None:
            raise Exception('No tweet with id = ' + id.__str__())
        if tweet.__getattribute__('lang') != 'en':
            return
        tweet = clearTweetJson(tweet._json)
        self.tweets.insert_one(tweet)
        if (to_print):
            print("Tweet :")
            print(tweet)
            print("is saved")
        if (with_author):
            self.saveUser(screen_name=tweet['screen_name'], to_print=to_print)
        return tweet

    # Zapisuje Tweet, replies, author(opcjonalnie),  authors of replies (opcjonalnie)
    def saveTweetWithAllData(self, id=-1, to_print=False, with_author=True, with_authors_of_replies=False):
        self.saveTweet(id, to_print=to_print)
        tweet = self.tweets.find_one({'id': id})
        self.saveUser(tweet['screen_name'], to_print=to_print)
        self.saveReplies(tweet, to_print=to_print, with_author=with_authors_of_replies)

    # Zapisuje Odpowiedzi do tweeta  ------- argument tweet to FAKTYCZNIE TWEET, NIE ID
    # def saveReplies(self,tweet,to_print=False,with_author=False):
    #     before_count =self.tweets.count()
    #     i=0
    #     cursor = tweepy.Cursor(tweepy.api.search, q='to:'+tweet['screen_name'],
    #                             since_id=tweet['id']).items()
    #     for reply in cursor:
    #         if i>=self.max_reply:
    #             break
    #         if (reply._json['in_reply_to_status_id']==tweet['id']):
    #             self.saveTweet(reply._json['id'],to_print=to_print,with_author=with_author)
    #
    #     if (to_print):
    #         print((self.tweets.count()-before_count).__str__()+' replies added\n')
    def saveReplies(self, tweet, to_print=False, with_author=False):
        before_count = self.tweets.count()
        i = 0
        cursor = tweepy.Cursor(self.api.search, q='to:' + tweet['screen_name'].__str__(),
                               since_id=tweet['id'],
                               result_type='recent',
                               limit=self.max_reply).items()  # Dlaczego tak mało zwraca odpowiedzi !! ?? Przez result_type
        for reply in cursor:
            if i > self.max_reply:
                break
            if (reply._json['in_reply_to_status_id'] == tweet['id']):
                self.saveTweet(reply._json['id'], to_print=to_print, with_author=with_author)
            i = i + 1
        cursor = tweepy.Cursor(self.api.search, q='to:' + tweet['screen_name'].__str__(),
                               since_id=tweet['id'],
                               result_type='popular',
                               limit=self.max_reply).items()  # Dlaczego tak mało zwraca odpowiedzi !! ?? Przez result_type
        i = 0
        for reply in cursor:
            if i > self.max_reply:
                break
            if (reply._json['in_reply_to_status_id'] == tweet['id']):
                self.saveTweet(reply._json['id'], to_print=to_print, with_author=with_author)
            i = i + 1

        if (to_print):
            print((self.tweets.count() - before_count).__str__() + ' replies added\n')

    # Zapisuje Tweety, które są poszukując ich na zasadzie wystąpywania słów, można zaostrzyć filtrem tylko zweryfikowani autorzy
    def saveTweetsWithWords(self, words, connected_with_tweet=id, limit=5,
                            verified_authors_only=False, with_authors=False, to_print=False):
        words = words + "-filter:retweets"
        cursor = tweepy.Cursor(self.api.search, q=words, lang='en', result_type='recent',tweet_mode="extended", timeout=999999).items(limit)
        tweets = []
        i = 0
        while True:
            if i >= limit:
                return tweets
            try:
                tweet = cursor.next()
                tweet = clearTweetJson(tweet._json, connected_with_tweet)
                if tweet['id'] == connected_with_tweet:
                    break
                user = self.api.get_user(screen_name=tweet['screen_name'])
                user = clearUserJson(user._json)
                if verified_authors_only:
                    if (user['verified']):
                        self.tweets.insert_one(tweet)
                        if (to_print):
                            print("Tweet :")
                            print(tweet["full_text"],print["screen_name"])
                            print("is saved")
                        if (with_authors):
                            self.users.insert_one(user)
                            if (to_print):
                                print("User :")
                                print(user)
                                print("is saved")

                else:
                    self.tweets.insert_one(tweet)
                    if (to_print):
                        print("Tweet :")
                        print(tweet["full_text"])
                        print("is saved")
                    if (with_authors):
                        self.users.insert_one(user)
                        if (to_print):
                            print("User :")
                            print(user)
                            print("is saved")
                i = i + 1
            except StopIteration:
                return

    # Zapisuje autora Tweetu
    def saveAuthor(self, id):
        tweet = self.api.get_status(id=id, tweet_mode='extended')
        self.users.insert_one(clearUserJson(self.api.get_user(screen_name=tweet.author.screen_name)))

    def loadDataForTweet(self, id, to_print=False, with_authors_of_replies=False, connected_tweets=True,
                         with_connected_tweets=False, verified_authors_only=False):
        tweet_count_before = self.tweets.count()
        user_count_before = self.tweets.count()
        self.saveTweetWithAllData(id=id, with_authors_of_replies=with_authors_of_replies, to_print=to_print)
        tweet_count_middle = self.tweets.count()
        user_count_middle = self.tweets.count()
        if connected_tweets:
            text = self.tweets.find_one({'id': id})['full_text']

            nazwy_wlasne = Cleaner.nazwy_wlasne(text)
            string = ' '.join(nazwy_wlasne)
            string = ' '.join(word for word in string.split() if len(word) > 2) # dluzsze niz 2 litery
            string = string.split()[:4] # 4 pierwsze slowa
            string = ' '.join(string)
            print(string)
            self.saveTweetsWithWords(string, connected_with_tweet=id, limit=10,
                                     verified_authors_only=verified_authors_only, to_print=to_print,
                                     with_authors=with_authors_of_replies)
        tweet_count_end = self.tweets.count()
        user_count_end = self.tweets.count()
        if to_print:
            print()
            print("There are " + tweet_count_end.__str__() + " tweets in the DB")
            print("There are " + user_count_end.__str__() + " users in the DB")
        print((tweet_count_end - tweet_count_middle).__str__() + " connected tweets")


# 1133284566632787969
if __name__ == '__main__':
    mongo = TweetLoader(restart=True, max_reply=10000)
    mongo.loadDataForTweet(id=-1, to_print=True, with_authors_of_replies=True, with_connected_tweets=True)
    # Pobieranie konkretnego tweeta, bez autora
    # mongo.saveTweet(id=1133184409127989248,to_print=True,with_author=False)

    # Pobieranie konkretnego użytkonika
    # mongo.saveUser(screen_name='potus',to_print=True)
    # Pobieranie konkretnego tweetu, jego autora, odpowiedziami do tweetu i ich autorami
    # mongo.saveTweetWithAllData(id=1133184409127989248,with_authors_of_replies=True,to_print=True)

    # Działanie pobierania tweetów powiązanych
    # mongo.saveTweetsWithWords(['Oklahoma','Japan'],connected_with_tweet='z tym ID',limit=100,verified_authors_only=True,to_print=True,with_authors=True)
