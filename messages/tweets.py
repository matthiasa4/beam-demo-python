import json
from datetime import datetime


class Tweet:

    def __init__(self, timestamp, tweet_id, text, user_id, user_name, entities, language):
        self.timestamp = timestamp
        self.tweet_id = tweet_id
        self.text = text
        self.user_id = user_id
        self.user_name = user_name
        self.entities = entities
        self.language = language

    @classmethod
    def contruct_tweet_from_json(cls, data):
        json_data = json.loads(data)
        t = cls(float(json_data["timestamp_ms"]),
                    json_data["id"],
                    json_data["text"],
                    json_data["user"]["id"],
                    json_data["user"]["screen_name"],
                    json_data["entities"],
                    json_data["lang"],
                    )

        return t

