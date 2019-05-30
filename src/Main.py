from src.mongoDB.fetcher import Fetcher
from src.mongoDB.tweetLoader import TweetLoader
from src.postCredibility import postCredibility
from src.twitter.BotChecket import BotChecker
from src.machinelearning.Predictor import Predictor
if __name__ == '__main__':
    id = 1134114931970838529
    mongo=TweetLoader(restart=True,max_reply=100)
    # mongo.saveTweetWithAllData(id=1133284566632787969,with_authors_of_replies=True,to_print=True)
    mongo.saveTweetWithAllData(id, to_print=False,with_authors_of_replies=True, connected_tweets=True,verified_authors_only=True,size_for_bot=15)
    fetcher = Fetcher()
    #fetcher.print_stats()
    pC = postCredibility()
    result = pC.evaluate(id)
    print(result)

    predictor = Predictor()
    Label_and_truth_prob= predictor.predict('This is example sentence.')

    bot_checker = BotChecker()
    is_bot_result = bot_checker.is_fake_based_on_user(id)
    malicious_urls_machine_learning = bot_checker.is_fake_based_on_external_urls(id, True)
    malicious_urls = bot_checker.is_fake_based_on_external_urls(id, False)
    print('is tweet fake result based on detecting bot:')
    print(is_bot_result)
    print('is tweet fake result based on external urls(with machine learning):')
    print(malicious_urls_machine_learning)
    print('is tweet fake result based on external urls(withou machine learning):')


    print('\nGłówny tweet:')
    print(fetcher.get_tweet(id=id))
    print('\nAutora:')
    print(fetcher.get_author_of_tweet(id=id))
    print('\n')
    # fetcher.print_users()
