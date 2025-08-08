import singer
import requests
import json

REQUIRED_CONFIG_KEYS = ["access_token", "start_date"]

schema = {'type': 'object',
    'properties':
      {
        'id': {'type': 'string'},
        'day': {'type': 'string'},
        'bedtime_start': {'type': 'string', 'format': 'date-time'},
        'bedtime_end': {'type': 'string', 'format': 'date-time'},
        'awake': {'type': 'integer'},
        'average_breath': {'type': 'number'},
        'heart_rate': {'interval': 'number', "item": {"type": ["null", "integer"]}, "timestamp": "string"},
        'hrv': {'interval': 'number', "item": {"type": ["null", "integer"]}, "timestamp": "string"},
        'average_heart_rate': {'type': 'number'},
        'lowest_heart_rate': {'type': 'number'},
        'average_hrv': {'type': 'number'},
        'sleep_analysis_reason': {"type": "string"},
        'period': {'type': 'number'},
        'deep_sleep_duration': {'type': 'integer'},
        'light_sleep_duration': {'type': 'integer'},
        'restless_periods': {'type': 'integer'},
        'rem_sleep_duration': {'type': 'integer'},
        'sleep_algorithm_version': {'type': 'string'},
        'low_battery_alert': {"type": "boolean"},
        'sleep_score_delta': {'type': 'integer'},
        'movement_30_sec': {'type': 'string'},
        'sleep_phase_5_min': {'type': 'string'},
        'efficiency': {'type': 'integer'},
        'total_sleep_duration': {'type': 'number'},
        'time_in_bed': {'type': 'number'},
        'type': {'type': 'string'},
        'latency': {'type': 'number'},
        'awake_time': {'type': 'number'},
        'readiness_score_delta': {'type': 'number'},
        'readiness': {
          "contributors": {
            "activity_balance": {'type': 'number'},
            "body_temperature": {'type': 'number'},
            "hrv_balance": {'type': 'number'},
            "previous_day_activity": {'type': 'number'},
            "previous_night": {'type': 'number'},
            "recovery_index": {'type': 'number'},
            "resting_heart_rate": {'type': 'number'},
            "sleep_balance": {'type': 'number'}
          },
          "score": {'type': 'number'},
          "temperature_deviation": {'type': 'number'},
          "temperature_trend_deviation": {'type': 'number'}
        }
      }}

def get_catalog(schema):
  streams = []

  for schema_name, schema in schema['properties'].items():
    catalog_entry = {
            'stream': schema_name,
            'tap_stream_id': schema_name,
            'schema': schema,
            'metadata': [], 
            'key_properties': 'id' 
    }
    streams.append(catalog_entry) 

  return {'streams': streams}

def do_discover(schema):
  catalog = get_catalog(schema)
  print(json.dumps(catalog, indent=2))

def do_sync(config, schema):

  access_token = config['access_token'] 
  start_date = config['start_date']

  singer.write_schema('sleeps', schema, 'id')

  headers = {"Authorization": f"Bearer {access_token}"}

  resp = requests.get('https://api.ouraring.com/v2/usercollection/sleep?start_date=%s' % (start_date), headers=headers)

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
