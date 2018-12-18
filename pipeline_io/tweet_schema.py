from apache_beam.io.gcp.internal.clients import bigquery

table_schema = bigquery.TableSchema()

timestamp_schema = bigquery.TableFieldSchema()
timestamp_schema.name = 'timestamp'
timestamp_schema.type = 'float'
timestamp_schema.mode = 'required'
table_schema.fields.append(timestamp_schema)

tweet_id_schema = bigquery.TableFieldSchema()
tweet_id_schema.name = 'tweet_id'
tweet_id_schema.type = 'integer'
tweet_id_schema.mode = 'required'
table_schema.fields.append(tweet_id_schema)

text_schema = bigquery.TableFieldSchema()
text_schema.name = 'text'
text_schema.type = 'string'
text_schema.mode = 'nullable'
table_schema.fields.append(text_schema)

# User nested field
user_schema = bigquery.TableFieldSchema()
user_schema.name = 'user'
user_schema.type = 'record'
user_schema.mode = 'nullable'

id_schema = bigquery.TableFieldSchema()
id_schema.name = 'id'
id_schema.type = 'string'
id_schema.mode = 'nullable'
user_schema.fields.append(id_schema)

name_schema = bigquery.TableFieldSchema()
name_schema.name = 'name'
name_schema.type = 'string'
name_schema.mode = 'nullable'
user_schema.fields.append(name_schema)
table_schema.fields.append(user_schema)

language_schema = bigquery.TableFieldSchema()
language_schema.name = 'language'
language_schema.type = 'string'
language_schema.mode = 'nullable'
table_schema.fields.append(language_schema)

