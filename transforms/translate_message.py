import json
import os

import apache_beam as beam
from google.cloud import translate
from google.oauth2 import service_account

from messages.log import Log

# credentials = service_account.Credentials.from_service_account_file(
#     os.path.join(os.path.dirname(__file__), os.pardir, 'conf', 'Matthias-Sandbox-be966dce6981.json'))


class TranslateMessage(beam.DoFn):
    def __init__(self, project_id):
        self.project_id = project_id

    def setup(self):
        self.translate_client = translate.TranslationServiceClient()

    def process(self, element):
        location = "global"
        parent = f"projects/{self.project_id}/locations/{location}"
        language_detected = self.translate_client.detect_language(
            content=element.text,
            parent=parent).languages[0]

        yield Log(element.timestamp,
                  element.text,
                  element.user_id,
                  language_detected.language_code,
                  language_detected.confidence
                  )
