import json
import requests
import socket
import sys
import os

# List of API endpoints:
# https://service.us2.sumologic.com/help/Default.htm#Sumo_Logic_Endpoints.htm%3FTocPath%3DAPIs%7C_____1
API_URL = 'https://api.us2.sumologic.com/api/v1/collectors'

USER = os.environ['SL_ACCESSID']
PASS = os.environ['SL_ACCESSKEY']
sources_file = sys.argv[1]

def post_source(collector_id):
    with open(sources_file) as json_file:
        json_data = json.load(json_file)
        for source in json_data['sources']:
            source_json = json.dumps(source)
            r = requests.post(API_URL + '/' + collector_id + '/sources', data=source_json, auth=(USER, PASS), headers={'content-type': 'application/json'}, verify=True)
            r.raise_for_status()

r = requests.get(API_URL, auth=(USER, PASS), verify=True)
r.raise_for_status()
collectors = r.json()
for collector in collectors['collectors']:
    collector_name = str(collector['name'])
    if '_aws_' in collector_name: continue
    print('Adding Sources to ' + collector_name)
    collector_id = str(collector['id'])
    post_source(collector_id)

