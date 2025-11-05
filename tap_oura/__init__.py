import singer
import requests
import json

REQUIRED_CONFIG_KEYS = ["access_token", "start_date"]

schema = {
  "type": "object",
  "properties": {
    "id": { "type": ["null", "string"] },
    "day": { "type": ["null", "string"] },
    "bedtime_start": { "type": ["null", "string"], "format": "date-time" },
    "bedtime_end": { "type": ["null", "string"], "format": "date-time" },
    "awake": { "type": ["null", "integer"] },
    "average_breath": { "type": ["null", "number"] },
    "heart_rate": {
      "type": ["null", "object"],
      "properties": {
        "interval": { "type": ["null", "number"] },
        "items": {
          "type": ["null", "array"],
          "items": { "type": ["null", "number"] }
        },
        "timestamp": { "type": ["null", "string"] }
      }
    },
    "hrv": {
      "type": ["null", "object"],
      "properties": {
        "interval": { "type": ["null", "number"] },
        "items": {
          "type": ["null", "array"],
          "items": { "type": ["null", "number"] }
        },
        "timestamp": { "type": ["null", "string"] }
      }
    },
    "average_heart_rate": { "type": ["null", "number"] },
    "lowest_heart_rate": { "type": ["null", "number"] },
    "average_hrv": { "type": ["null", "number"] },
    "sleep_analysis_reason": { "type": ["null", "string"] },
    "period": { "type": ["null", "number"] },
    "deep_sleep_duration": { "type": ["null", "integer"] },
    "light_sleep_duration": { "type": ["null", "integer"] },
    "restless_periods": { "type": ["null", "integer"] },
    "rem_sleep_duration": { "type": ["null", "integer"] },
    "sleep_algorithm_version": { "type": ["null", "string"] },
    "low_battery_alert": { "type": ["null", "boolean"] },
    "sleep_score_delta": { "type": ["null", "integer"] },
    "movement_30_sec": { "type": ["null", "string"] },
    "sleep_phase_5_min": { "type": ["null", "string"] },
    "efficiency": { "type": ["null", "integer"] },
    "total_sleep_duration": { "type": ["null", "number"] },
    "time_in_bed": { "type": ["null", "number"] },
    "type": { "type": ["null", "string"] },
    "latency": { "type": ["null", "number"] },
    "awake_time": { "type": ["null", "number"] },
    "readiness_score_delta": { "type": ["null", "number"] },
    "readiness": {
      "type": ["null", "object"],
      "properties": {
        "contributors": {
          "type": ["null", "object"],
          "properties": {
            "activity_balance": { "type": ["null", "number"] },
            "body_temperature": { "type": ["null", "number"] },
            "hrv_balance": { "type": ["null", "number"] },
            "previous_day_activity": { "type": ["null", "number"] },
            "previous_night": { "type": ["null", "number"] },
            "recovery_index": { "type": ["null", "number"] },
            "resting_heart_rate": { "type": ["null", "number"] },
            "sleep_balance": { "type": ["null", "number"] }
          }
        },
        "score": { "type": ["null", "number"] },
        "temperature_deviation": { "type": ["null", "number"] },
        "temperature_trend_deviation": { "type": ["null", "number"] }
      }
    }
  }
}

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
