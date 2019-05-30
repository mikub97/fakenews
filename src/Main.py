from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader
from src.postCredibility import postCredibility
from src.UserVerification import verifyUser
if __name__ == '__main__':
    id = 1134048673330077697
    screen_name ='ABC'
    mongo=TweetLoader(restart=True,max_reply=100)
    # mongo.saveTweetWithAllData(id=1133284566632787969,with_authors_of_replies=True,to_print=True)
    mongo.loadDataForTweet(id, to_print=False,with_authors_of_replies=True, with_connected_tweets=True)
    fetcher = Fetcher()
    #fetcher.print_stats()
    # pC = postCredibility()
    # pC.evaluate(id)
    print('\nGłówny tweet:')
    print(fetcher.get_tweet(id=id))
    print('\nAutora:')
    print(fetcher.get_author_of_tweet(id=id))
    print(verifyUser(screen_name))
    print('\n')
    # fetcher.print_users()
