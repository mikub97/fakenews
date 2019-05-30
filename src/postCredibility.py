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

        print(tweetJson)
        text = tweetJson["full_text"]
        tweetSentiment = Cleaner.getTweetSentiments(text)
        tweetSubjectivity = Cleaner.getTweetSubjectivity(text)
        sentimentComments = 0;
        subjectivityComments = 0
        i = 0
        #
        repliesJson = fetcher.get_replies(id)
        if repliesJson:
            for reply in repliesJson:
                i = i + 1
                replyText = reply["full_text"]
                sentimentComments = sentimentComments + Cleaner.getTweetSentiments(replyText)
                subjectivityComments = subjectivityComments + Cleaner.getTweetSubjectivity(replyText)
            meanSentimentComments = sentimentComments / i
            meanSubjectivityComments = subjectivityComments / i
            print("Mean comments subjectivity: ", meanSubjectivityComments, "Mean comments Sentiment: ",
                  meanSentimentComments)
        print("Sentiment: ", tweetSentiment, "Subjectivity: ", tweetSubjectivity)

        connectedTweets = fetcher.get_connected(id)
        i = 0
        for connectedTweet in connectedTweets:
            author = fetcher.get_author_of_tweet(connectedTweet["id"])
            if str(author["verified"]) == "True":
                i = i + 1
        percentVerifiedComments = i / len(connectedTweets)
        print("Percent verified users with similar tweet: ", i / (len(connectedTweets)))
        numOfFavs = tweetJson["favorite_count"]
        tweetAuthor = fetcher.get_author_of_tweet(tweetJson["id"])
        numOfFollowers = tweetAuthor["followers_count"]
        numOfRT = tweetJson['retweet_count']
        print(numOfFollowers, numOfFavs, numOfRT)
        Dict = {"FakeProbability":0, "Details":"lol"}
        pts = 210;
        if (percentVerifiedComments > 0.2): pts = pts + 100
        if numOfFavs > 10:
            pts = pts + 70
        if numOfRT > 100: pts = pts + 80
        if numOfFollowers > 1000: pts = pts + 80
        if pts > 250: Dict["Details"] = "Tweet is popular. High chance it is not fake."
        else: Dict["Details"] = "Tweet does not have relevance. It is in risk group."
        pts = (pts - abs(tweetSubjectivity * 105) - abs(105 * tweetSentiment))/420
        Dict["FakeProbability"] = 1-pts
        return Dict
