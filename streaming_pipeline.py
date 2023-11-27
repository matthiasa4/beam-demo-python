from __future__ import absolute_import

import argparse
import json
import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.transforms import trigger

from aggregates.language_aggregate import LanguageAggregate
from aggregates.user_aggregate import UserAggregate
from pipeline_io import json_schema, json_to_bqrecords
from transforms.message_to_log import MessageToLog
from transforms.translate_message import TranslateMessage


def run(argv=None):
    # Add command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output', required=True,
        help='Output BigQuery table for results specified as: PROJECT:DATASET.TABLE or DATASET.TABLE.')

    parser.add_argument(
        '--input_subscription', required=True,
        help='Input PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."')

    parser.add_argument(
        '--output_subscription', required=True,
        help='Output PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."')

    known_args, pipeline_args = parser.parse_known_args(argv)

    # Set pipeline options
    pipeline_options = PipelineOptions(pipeline_args)
    project_id = pipeline_options.get_all_options()['project']
    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    p = beam.Pipeline(options=pipeline_options)

    # Main pipeline: read in Logs, write them to BigQuery
    message_table = 'logs'
    messages = (p
                | 'Read from PubSub' >>
                beam.io.ReadFromPubSub(subscription=known_args.input_subscription).with_output_types(bytes)
                | 'Decode messages' >> beam.Map(lambda x: x.decode('utf-8'))
                | 'Parse messages to Logs ' >> beam.ParDo(MessageToLog())
                | 'Detect language' >> beam.ParDo(TranslateMessage(project_id))

    (messages   | 'Convert Log to BigQuery records' >> beam.Map(json_to_bqrecords.json_to_bqrecord)
                | 'Write Logs to BigQuery' >> beam.io.WriteToBigQuery(
                       known_args.output + message_table,
                       schema=json_schema.log_table_schema,
                       create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                       write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

    # Calculate aggregates per language, write to BigQuery
    language_aggregate_table = 'languages'
    languages = (messages   | 'Extract language tuple' >> (beam.Map(lambda x: (x.translate_language, x)))
                | 'Assign Fixed Windows' >> beam.WindowInto(window.FixedWindows(60, 0),
                                                            trigger=trigger.AfterWatermark(),
                                                            accumulation_mode=trigger.AccumulationMode.ACCUMULATING)
                | 'GroupByKey Languages' >> beam.GroupByKey()
                | 'Count languages' >> beam.ParDo(LanguageAggregate())
                )

    (languages  | 'Convert language aggregate to BigQuery records' >> beam.Map(json_to_bqrecords
                                                                               .language_aggregate_to_bqrecords)
                | 'Write LanguageAggregate to BigQuery' >> beam.io.WriteToBigQuery(
                    known_args.output + language_aggregate_table,
                    schema=json_schema.language_table_schema,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

    (languages      | 'Convert language aggregate to PubSub message' >> beam.Map(json_to_bqrecords
                                                                               .language_aggregate_to_pubsubmessage)
                    | 'Encode' >> beam.Map(lambda x: json.dumps(x, ensure_ascii=False).encode('utf-8'))
                                        .with_output_types(bytes)
                    | 'Write LanguageAggregate to PubSub' >> beam.io.WriteToPubSub(known_args.output_subscription))

    # Calculate aggregates per user, write to
    user_aggregate_table = 'users'
    (messages   | 'Extract user tuple' >> (beam.Map(lambda x: (x.user_id, x)))
                | 'Assign Sessions' >> beam.WindowInto(window.Sessions(30),
                                                       trigger=trigger.AfterWatermark(),
                                                       accumulation_mode=trigger.AccumulationMode.ACCUMULATING)
                | 'GroupByKey Users' >> beam.GroupByKey()
                | 'Count user' >> beam.ParDo(UserAggregate())
                | 'Convert user aggregate to BigQuery records' >> beam.Map(json_to_bqrecords
                                                                               .user_aggregate_to_bqrecords)
                | 'Write UserAggregate to BigQuery' >> beam.io.WriteToBigQuery(
                known_args.output + user_aggregate_table,
                schema=json_schema.user_table_schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            ))

    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
