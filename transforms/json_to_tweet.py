import apache_beam as beam

from messages.tweets import Tweet


class JSONToTweetDoFn(beam.DoFn):

    def process(self, element):
        yield Tweet.contruct_tweet_from_json(element)
