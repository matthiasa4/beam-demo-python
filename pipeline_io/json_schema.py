from apache_beam.io.gcp.internal.clients import bigquery

# Tableschema for logs
log_table_schema = bigquery.TableSchema()

timestamp_schema = bigquery.TableFieldSchema()
timestamp_schema.name = 'timestamp'
timestamp_schema.type = 'float'
timestamp_schema.mode = 'nullable'
log_table_schema.fields.append(timestamp_schema)

user_id_schema = bigquery.TableFieldSchema()
user_id_schema.name = 'user_id'
user_id_schema.type = 'string'
user_id_schema.mode = 'nullable'
log_table_schema.fields.append(user_id_schema)

text_schema = bigquery.TableFieldSchema()
text_schema.name = 'text'
text_schema.type = 'string'
text_schema.mode = 'nullable'
log_table_schema.fields.append(text_schema)

# Language nested field
language_schema = bigquery.TableFieldSchema()
language_schema.name = 'language'
language_schema.type = 'record'
language_schema.mode = 'nullable'

translate_language_schema = bigquery.TableFieldSchema()
translate_language_schema.name = 'translate_language'
translate_language_schema.type = 'string'
translate_language_schema.mode = 'nullable'
language_schema.fields.append(translate_language_schema)

translate_confidence_schema = bigquery.TableFieldSchema()
translate_confidence_schema.name = 'translate_confidence'
translate_confidence_schema.type = 'string'
translate_confidence_schema.mode = 'nullable'
language_schema.fields.append(translate_confidence_schema)

log_table_schema.fields.append(language_schema)

# Tableschema for languages
language_table_schema = bigquery.TableSchema()

window_schema = bigquery.TableFieldSchema()
window_schema.name = 'window'
window_schema.type = 'string'
window_schema.mode = 'nullable'
language_table_schema.fields.append(window_schema)

language_schema = bigquery.TableFieldSchema()
language_schema.name = 'language'
language_schema.type = 'string'
language_schema.mode = 'nullable'
language_table_schema.fields.append(language_schema)

count_schema = bigquery.TableFieldSchema()
count_schema.name = 'count'
count_schema.type = 'integer'
count_schema.mode = 'nullable'
language_table_schema.fields.append(count_schema)

# Tableschema for user
user_table_schema = bigquery.TableSchema()

user_id_schema = bigquery.TableFieldSchema()
user_id_schema.name = 'user_id'
user_id_schema.type = 'string'
user_id_schema.mode = 'nullable'
user_table_schema.fields.append(user_id_schema)

window_schema = bigquery.TableFieldSchema()
window_schema.name = 'window'
window_schema.type = 'string'
window_schema.mode = 'nullable'
user_table_schema.fields.append(window_schema)

number_of_sentences_schema = bigquery.TableFieldSchema()
number_of_sentences_schema.name = 'number_of_sentences'
number_of_sentences_schema.type = 'integer'
number_of_sentences_schema.mode = 'nullable'
user_table_schema.fields.append(number_of_sentences_schema)

number_of_languages_schema = bigquery.TableFieldSchema()
number_of_languages_schema.name = 'number_of_languages'
number_of_languages_schema.type = 'integer'
number_of_languages_schema.mode = 'nullable'
user_table_schema.fields.append(number_of_languages_schema)

average_time_between_schema = bigquery.TableFieldSchema()
average_time_between_schema.name = 'average_time_between'
average_time_between_schema.type = 'float'
average_time_between_schema.mode = 'nullable'
user_table_schema.fields.append(average_time_between_schema)

total_session_length_schema = bigquery.TableFieldSchema()
total_session_length_schema.name = 'total_session_length'
total_session_length_schema.type = 'float'
total_session_length_schema.mode = 'nullable'
user_table_schema.fields.append(total_session_length_schema)
