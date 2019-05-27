import json
import re
from src.twitter.TwitterConncection import TwitterConnection
import tweepy
import pymongo
from textblob import TextBlob

def clean_tweet( tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                           "|(\w+:\/\/\S+)",
                           " ",
                           tweet).split())


def getTweetSentiments(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity



def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["tweets"]
    # TwitterConncection object
    api2 = TwitterConnection()
    api = tweepy.API(api2.auth)

    # search =  api.user_timeline(screen_name = 'realDonaldTrump', count = 1, include_rts = True,tweet_mode="extended")
    search = tweepy.Cursor(api.search, q="Trump News -filter:retweets", lang="en", show_user="true",
                           tweet_mode="extended").items(10)
    for item in search:
        user = api.get_user(item.user.screen_name)
        text = item.full_text
        username = item.user.screen_name
        id = item.id

        followCount = user.followers_count
        friendsCount = user.friends_count
        RTcount = item.retweet_count
        creationDate = item.created_at
        sentiment = getTweetSentiments(text)
        """print(sentiment)
        print(item.full_text)
        print(item.id)
        print("folcount: ", user.followers_count)
        print("frencount: ", user.friends_count)
        print(item.created_at)
        print(item.retweet_count)
        print("retweets: ", item.retweet_count)
        print(item.user.screen_name)

        print(text)
        print(username) """
        potentialreplies = tweepy.Cursor(api.search, q='to:{}'.format(username),
                                         since_id=id, tweet_mode='extended').items()
        count = 0
        replies = []
        while True:
            if count == 10: break
            try:
                reply = potentialreplies.next()
                if not hasattr(reply, 'in_reply_to_status_id_str'):
                    print("no replies")
                if reply.in_reply_to_status_id == id:
                    count = count + 1
                    print("reply of tweet:{}".format(reply.full_text))
                    replies.append(reply.full_text)

            except tweepy.RateLimitError as e:
                print("Twitter api rate limit reached".format(e))
                continue

            except tweepy.TweepError as e:
                print("Tweepy error occured:{}".format(e))
                break

            except StopIteration:
                # if replies == []: print("no replies")
                break

            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                break
        json = {}
        json["id"] = id
        json["text"] = text
        json["sentiment"] = sentiment
        json["friendsCount"] = friendsCount
        json["followersCount"] = followCount
        json["comments"] = replies
        json["retweetCount"] = RTcount
        json["username"] = username
        json["date"] = creationDate
        print(json)
        mycol.insert_one(json)
    print("done")


if __name__ == '__main__':
    main()
