import json

import apache_beam as beam

from messages.log import Log


class MessageToLog(beam.DoFn):

    def process(self, element, timestamp=beam.DoFn.TimestampParam):
        json_element = json.loads(element)
        yield Log(float(timestamp),
                  json_element['text'],
                  json_element['userId']
                  )

