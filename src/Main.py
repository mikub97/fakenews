from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader

if __name__ == '__main__':
    mongo=TweetLoader(restart=True)
    mongo.saveTweetWithAllData(id=1133284566632787969,with_author_of_replies=True)

    fetcher = Fetcher()
    fetcher.print_stats()
    print('\n')
    fetcher.print_tweets()
    print('\n')
    fetcher.print_users()