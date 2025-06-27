import singer
import requests
import json

REQUIRED_CONFIG_KEYS = ["access_token", "start_date"]

schema = {'type': 'object',
    'properties':
      {
        'bedtime_start': {'type': 'string', 'format': 'date-time'},
        'bedtime_end': {'type': 'string', 'format': 'date-time'},
        'bedtime_start_delta': {'type': 'integer'},
        'bedtime_end_delta': {'type': 'integer'},
        'awake': {'type': 'integer'},
        'breath_average': {'type': 'number'},
        'deep': {'type': 'integer'},
        'duration': {'type': 'integer'},
        'efficiency': {'type': 'integer'},
        "hr_5min": {"type": ["null", "array"], "items": {"type": ["null", "integer"]}},
        'hr_average': {'type': 'number'},
        'hr_lowest': {'type': 'integer'},
        'hypnogram_5min': {'type': 'string'},
        'is_longest': {'type': 'integer'},
        'light': {'type': 'integer'},
        'midpoint_at_delta': {'type': 'integer'},
        'midpoint_time': {'type': 'integer'},
        'onset_latency': {'type': 'integer'},
        'period_id': {'type': 'integer'},
        'rem': {'type': 'integer'},
        'restless': {'type': 'integer'},
        'rmssd': {'type': 'integer'},
        'rmssd_5min': {"type": ["null", "array"], "items": {"type": ["null", "integer"]}}, 
        'score': {'type': 'integer'},
        'score_alignment': {'type': 'integer'},
        'score_deep': {'type': 'integer'},
        'score_disturbances': {'type': 'integer'},
        'score_efficiency': {'type': 'integer'},
        'score_latency': {'type': 'integer'},
        'score_rem': {'type': 'integer'},
        'score_total': {'type': 'integer'},
        'summary_date': {'type': 'string'},
        'temperature_delta': {'type': 'number'},
        'temperature_deviation': {'type': 'number'},
        'temperature_trend_deviation': {'type': 'number'},
        'timezone': {'type': 'number'},
        'total': {'type': 'number'}
      }}

def get_catalog(schema):
  streams = []

  for schema_name, schema in schema['properties'].items():
    catalog_entry = {
            'stream': schema_name,
            'tap_stream_id': schema_name,
            'schema': schema,
            'metadata': [], 
            'key_properties': 'summary_date' 
    }
    streams.append(catalog_entry) 

  return {'streams': streams}

def do_discover(schema):
  catalog = get_catalog(schema)
  print(json.dumps(catalog, indent=2))

def do_sync(config, schema):

  access_token = config['access_token'] 
  start_date = config['start_date']

  singer.write_schema('sleeps', schema, 'summary_date')

  headers = {"Authorization": f"Bearer {access_token}"}

  resp = requests.get('https://api.ouraring.com/v2/usercollection/sleep?start_date=%s' % (start_date))
  print('HELLO', resp)
  sleeps = resp.json()['data']

  for sleep in sleeps:
    singer.write_record('sleeps', sleep)

def main():
  args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

  if args.discover:
    do_discover(schema)
  else:
    do_sync(args.config, schema)

if __name__ == '__main__':
  main()
