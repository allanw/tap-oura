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
        'bedtime_start_delta': 'interger',
        'bedtime_end_delta': 'integer',
        'awake': 'integer',
        'breath_average': 'number',
        'deep': 'integer',
        'duration': 'integer',
        'efficiency': 'integer',
        'hr_5min': 'object',
        'hr_average': 'number',
        'hr_lowest': 'integer',
        'hypnogram_5min': 'object',
        'is_longest': 'integer',
        'light': 'integer',
        'midpoint_at_delta': 'integer',
        'midpoint_time': 'integer',
        'onset_latency': 'integer',
        'period_id': 'integer',
        'rem': 'integer',
        'restless': 'integer',
        'rmssd': 'integer',
        'rmssd_5min': 'object',
        'score': 'integer',
        'score_alignment': 'integer',
        'score_deep': 'integer',
        'score_disturbances': 'integer',
        'score_efficiency': 'integer',
        'score_latency': 'integer',
        'score_rem': 'integer',
        'score_total': 'integer',
        'summary_date': 'string',
        'temperature_delta': 'number',
        'temperature_deviation': 'number',
        'temperature_trend_deviation': 'number',
        'timezone': 'number',
        'total': 'number'
      }}

  singer.write_schema('sleeps', schema, 'summary_date')

  resp = requests.get('https://api.ouraring.com/v1/sleep?start=%s&access_token=%s' % (start_date, access_token))

  sleeps = resp.json()['sleep']

  for sleep in sleeps:
    singer.write_record('sleep', sleep)

