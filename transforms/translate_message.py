import json
import os

import apache_beam as beam
from google.cloud import translate
from google.oauth2 import service_account

from messages.log import Log

# credentials = service_account.Credentials.from_service_account_file(
#     os.path.join(os.path.dirname(__file__), os.pardir, 'conf', 'Matthias-Sandbox-be966dce6981.json'))


class TranslateMessage(beam.DoFn):

    def process(self, element):
        # translate_client = translate.Client(credentials=credentials)
        translate_client = translate.Client()
        language_detected = translate_client.detect_language(element.text)
        print str(language_detected)
        yield Log(element.timestamp,
                  element.text,
                  element.user_id,
                  language_detected['language'],
                  language_detected['confidence'])

