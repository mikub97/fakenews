from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader
from src.postCredibility import postCredibility
if __name__ == '__main__':
    id = 1134114931970838529
    mongo=TweetLoader(restart=True,max_reply=100)
    # mongo.saveTweetWithAllData(id=1133284566632787969,with_authors_of_replies=True,to_print=True)
    mongo.saveTweetWithAllData(id, to_print=False,with_authors_of_replies=True, connected_tweets=True,verified_authors_only=True)
    fetcher = Fetcher()
    #fetcher.print_stats()
    pC = postCredibility()
    result = pC.evaluate(id)
    print(result)
    """
    print('\nGłówny tweet:')
    print(fetcher.get_tweet(id=1133699637678870528))
    print('\nAutora:')
    print(fetcher.get_author_of_tweet(id=1133699637678870528))
    print('\n')
    # fetcher.print_users()
    """