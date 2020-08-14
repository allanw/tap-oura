import singer
import requests
import json

REQUIRED_CONFIG_KEYS = ["access_token", "start_date"]

def main():

  args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

  config = args.config
  
  access_token = config['access_token'] 
  start_date = config['start_date']

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
        'hypnogram_5min': {'type': 'object'},
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

  singer.write_schema('sleeps', schema, 'summary_date')

  resp = requests.get('https://api.ouraring.com/v1/sleep?start=%s&access_token=%s' % (start_date, access_token))

  sleeps = resp.json()['sleep']

  for sleep in sleeps:
    singer.write_record('sleep', sleep)

