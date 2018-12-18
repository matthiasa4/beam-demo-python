class Log:

    def __init__(self, timestamp, text, user_id, translate_language=None, translate_confidence=None):
        self.timestamp = timestamp
        self.text = text
        self.user_id = user_id
        self.translate_language = translate_language
        self.translate_confidence = translate_confidence

