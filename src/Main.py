from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader
from src.postCredibility import postCredibility
if __name__ == '__main__':
    id = 1133083151885045760
    mongo=TweetLoader(restart=True,max_reply=100)
    # mongo.saveTweetWithAllData(id=1133284566632787969,with_authors_of_replies=True,to_print=True)
    mongo.loadDataForTweet(id, to_print=False,with_authors_of_replies=True, with_connected_tweets=True)
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