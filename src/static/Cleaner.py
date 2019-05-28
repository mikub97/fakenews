import json
import re

from textblob import TextBlob


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                           "|(\w+:\/\/\S+)",
                           " ",
                           tweet).split())


def getTweetSentiments(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity



def clearTweetJson(json,connected_with_tweet=None):
    toDeleteAttr = ['metadata','quoted_status','entities','id_str','user','place','favorited','retweeted',
                    'coordinates','contributors','source','truncated','geo','in_reply_to_status_id_str',
                    'in_reply_to_user_id','in_reply_to_user_id_str','_id','extended_entities','retweeted_status',
                        'quoted_status_id_str']

    json['user_mentions']=[]
    json['hashtags']=[]
    json['connected_with_tweet']=connected_with_tweet
    try :
        for user_mention in json['entities']['user_mentions']:
            json['user_mentions'].append(user_mention['screen_name'])
    except:
        pass
    try:
        json['screen_name']=json['user']['screen_name']
    except:
        pass
    try:
        for hash in json['entities']['hashtags']:
            json['hashtags'].append(hash['text'])
    except:
        pass
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

def clearUserJson(json):
    toDeleteAttr = ['metadata','quoted_status','entities','id_str','user','place','favorited','retweeted',
                    'coordinates','contributors','source','truncated','geo','in_reply_to_status_id_str',
                    'in_reply_to_user_id','in_reply_to_user_id_str','_id','extended_entities','retweeted_status',
                    'quoted_status_id_str','default_profile_image','status', "notifications",
                    "profile_background_color","profile_background_image_url", "profile_background_image_url_https",
                    "profile_background_tile","profile_banner_url","profile_image_url","profile_image_url_https",
                    "profile_link_color","profile_sidebar_border_color","profile_sidebar_fill_color","profile_text_color",
                    "profile_use_background_image","translator_type","url","utc_offset","id","follow_request_sent","default_profile"]
    for attr in toDeleteAttr:
        try:
            del json[attr]
        except:
            pass
    return json


