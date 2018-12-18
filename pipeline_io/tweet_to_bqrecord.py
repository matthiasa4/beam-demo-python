from messages.tweets import Tweet

def tweet_to_bqrecord(element):
    return \
        {'timestamp': element.timestamp,
            'tweet_id': element.tweet_id,
            'text': element.text,
            'user': {
                'id': element.user_id,
                'name': element.user_name,
            },
            'language': element.language,
        }
