import sys

from src.machinelearning.Predictor import Predictor
from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader
from src.postCredibility import postCredibility
from src.static.Cleaner import clearTweetJson
from src.twitter.BotChecket import BotChecker
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pass an id of a tweet to check')
    parser.add_argument('-id', dest='id', default=-112,
                        help='id of tweet for analysis')
    parser.add_argument('--restart', dest='restart', action='store_const',
                        const=True, default=False,
                        help='restarts mongoDB')
    parser.add_argument('--only-anal', dest='anal', action='store_const',
                        const=True, default=False,
                        help='if set there will be no more tweets loaded from twitter')
    anal = parser.parse_args().anal
    restart = parser.parse_args().restart
    id = int(parser.parse_args().id)
    if id==-112 :
        parser.print_usage()
        sys.exit()
    if (not anal):
        mongo=TweetLoader(restart=restart,max_reply=100)
        mongo.saveTweetWithAllData(id, to_print=False,with_authors_of_replies=True, connected_tweets=True,verified_authors_only=True,size_for_bot=15)


    fetcher = Fetcher()


    pC = postCredibility()
    result = pC.evaluate(id)
    print(result)

    predictor = Predictor()
    Label_and_truth_prob= predictor.predict('This is example sentence.')

    bot_checker = BotChecker()
    is_bot_result = bot_checker.is_fake_based_on_user(id)
    malicious_urls_machine_learning = bot_checker.is_fake_based_on_external_urls(id, True)
    malicious_urls = bot_checker.is_fake_based_on_external_urls(id, False)



    # print('\nGłówny tweet:')
    # print(clearTweetJson(fetcher.get_tweet(id=id),remove_entities=True))
    # print('\nAutora:')
    # print(fetcher.get_author_of_tweet(id=id))
    # print('\n')
    # # fetcher.print_users()
