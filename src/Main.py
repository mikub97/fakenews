from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader

if __name__ == '__main__':
    mongo=TweetLoader()
    mongo.saveTweetWithDataById(id=1133284566632787969)

    fetcher = Fetcher()
    fetcher.print_tweets()