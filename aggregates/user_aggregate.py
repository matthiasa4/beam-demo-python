import apache_beam as beam

class UserAggregate(beam.DoFn):

    # Element here will be a tuple (user, List of Logs)
    def process(self, element, window=beam.DoFn.WindowParam):
        user = element[0]
        logs = element[1]

        # Sort your logs on time
        logs.sort(key=lambda x: x.timestamp, reverse=False)

        languages = set()
        time_between = 0
        for i, l in enumerate(logs):
            languages.add(l.translate_language)
            if i > 0:
                time_between += l.timestamp - logs[i-1].timestamp

        total_session_length = logs[-1].timestamp - logs[0].timestamp

        yield (user,
               str(window),
               len(logs),
               len(languages),
               time_between / len(logs),
               total_session_length)
