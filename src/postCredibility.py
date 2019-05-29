import pymongo
from bson.json_util import dumps
from src.mongoDB.fetcher import Fetcher
from src.static import Cleaner
import src.static.Cleaner
from src.mongoDB.tweetLoader import TweetLoader


class postCredibility():

    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.tweets = self.mydb["tweets"]
        self.users = self.mydb['users']

    def evaluate(self, id):
        mongo = TweetLoader(restart=False)
        fetcher = Fetcher()
        tweetJson = fetcher.get_tweet(id)

        # print(tweetJson)
        text = tweetJson["full_text"]
        tweetSentiment = Cleaner.getTweetSentiments(text)
        tweetSubjectivity = Cleaner.getTweetSubjectivity(text)
        sentimentComments = 0;
        subjectivityComments = 0
        i = 0
        """
        repliesJson = fetcher.get_replies(id)
        if repliesJson:
            for reply in repliesJson:
                i = i + 1
                replyText = reply["full_text"]
                print(replyText)
                sentimentComments = sentimentComments + Cleaner.getTweetSentiments(replyText)
                subjectivityComments = subjectivityComments + Cleaner.getTweetSubjectivity(replyText)
            meanSentimentComments = sentimentComments / i
            meanSubjectivityComments = subjectivityComments / i
        print("Sentiment: ", tweetSentiment, "Mean comments Sentiment: ", meanSentimentComments)
        print("Subjectivity: ", tweetSubjectivity, "Mean comments subjectivity: ", meanSubjectivityComments)
        """
        connectedTweets = fetcher.get_connected(id)
        for connectedTweet in connectedTweets:
            print(connectedTweet)
        return text
