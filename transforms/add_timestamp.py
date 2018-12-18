import apache_beam as beam


class AddTimestampFn(beam.DoFn):
  def process(self, element):
    yield beam.window.TimestampedValue(element, element.timestamp / 1000.0)