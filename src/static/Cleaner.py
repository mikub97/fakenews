import re

from textblob import TextBlob


def clean_tweet(tweet):
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


def clearTweetJson(json):
    toDeleteAttr = ['metadata','quoted_status','entities','id_str','user','place','favorited','retweeted',
                    'coordinates','contributors','source','truncated','geo','in_reply_to_status_id_str',
                    'in_reply_to_user_id','in_reply_to_user_id_str','_id','extended_entities','retweeted_status',
                        'quoted_status_id_str']
    try:
        json['user_name']=json['user']['screen_name']
    except:
        pass
    try:
        json['hashtags']=json['entities']['hashtags']
    except:
        pass
    json['user_mentions']=[]
    try :
        for user_mention in json['entities']['user_mentions']:
            json['user_mentions'].append(user_mention['screen_name'])
    except:
        pass
    for attr in toDeleteAttr:
        try:
            del json[attr]
        except:
            pass
    return json