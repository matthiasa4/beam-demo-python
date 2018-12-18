from __future__ import absolute_import

import argparse
import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions

from transforms.json_to_tweet import JSONToTweetDoFn
from transforms.add_timestamp import AddTimestampFn
from conf.___conf__ import messages_path

def run(argv=None):
  """Build and run the pipeline."""
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--output', required=True,
      help=('Output BigQuery table for results specified as: PROJECT:DATASET.TABLE '
       'or DATASET.TABLE.'))
  parser.add_argument(
      '--input_subscription', required=True,
      help=('Input PubSub subscription of the form '
            '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'))
  known_args, pipeline_args = parser.parse_known_args(argv)

  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = True
  pipeline_options.view_as(StandardOptions).streaming = True
  p = beam.Pipeline(options=pipeline_options)

  # Read from PubSub into a PCollection.
  # messages = (p
  #               | beam.io.ReadFromPubSub(
  #                   subscription=known_args.input_subscription)
  #               .with_output_types(bytes))

  messages = (p
                | beam.io.ReadFromText(messages_path))

  lines = messages | 'decode' >> beam.Map(lambda x: x.decode('utf-8'))

  tweets = lines | 'extract tweets' >> (beam.ParDo(JSONToTweetDoFn()))

  tweets_with_ts = tweets | 'set timestamp' >> beam.ParDo(AddTimestampFn())

  # records = tweets | 'tweets to records' >> (beam.Map(tweet_to_bqrecord.tweet_to_bqrecord))

  def count(element):
    (w, ones) = element
    print (w, sum(ones))
    return (w, sum(ones))

  languages = (tweets_with_ts
                | 'extract language' >> (beam.Map(lambda x: (x.language, 1)))
                | beam.WindowInto(window.FixedWindows(1, 0))
                | 'group' >> beam.GroupByKey()
                | 'count' >> beam.Map(count)
                )

  # records | 'write' >> beam.io.Write(
  #     beam.io.BigQuerySink(
  #         known_args.output,
  #         schema=tweet_schema.table_schema,
  #         create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
  #         write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE))

  result = p.run()
  result.wait_until_finish()


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()