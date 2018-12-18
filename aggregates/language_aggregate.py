import apache_beam as beam


class LanguageAggregate(beam.DoFn):

    # Element here will be a tuple (user, List of Logs)
    def process(self, element, window=beam.DoFn.WindowParam):
        (language, ones) = element

        yield (str(window),
               language,
               len(ones))


