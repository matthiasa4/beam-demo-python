import json

def json_to_bqrecord(element):
    print(element)
    return \
        {
            'timestamp': element.timestamp,
            'user_id': element.user_id,
            'text': element.text,
            'language': {
                'translate_language': element.translate_language,
                'translate_confidence': element.translate_confidence
            }
        }


def language_aggregate_to_bqrecords(element):
    return \
        {
            'window': element[0],
            'language': element[1],
            'count': element[2]
        }

def language_aggregate_to_pubsubmessage(element):
    return \
        {
            'window_start': float(element[0].split(",")[0][1:])*1000,
            'window_end': float(element[0].split(",")[1][:-1])*1000,
            'language': element[1],
            'count': element[2]
        }


def user_aggregate_to_bqrecords(element):
    return \
        {
            'user_id': element[0],
            'window': element[1],
            'number_of_sentences': element[2],
            'number_of_languages': element[3],
            'average_time_between': element[4],
            'total_session_length': element[5]
        }
