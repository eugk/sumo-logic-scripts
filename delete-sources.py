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

def remove_sources(collector_id):
    r = requests.get(API_URL + '/' + collector_id + '/sources', auth=(USER, PASS), verify=True).json()
    sources = r['sources']
    for s in sources:
        if 'db_logs' in s['name']:
            print 'Removing source named ' + s['name']
            r2 = requests.delete(API_URL + '/' + collector_id + '/sources/' + str(s['id']), auth=(USER, PASS), verify=True)
            r2.raise_for_status()

r = requests.get(API_URL, auth=(USER, PASS), verify=True)
r.raise_for_status()
collectors = r.json()
for collector in collectors['collectors']:
    collector_name = str(collector['name'])
    if '_aws_' in collector_name: continue
    #print('Removing sources from ' + collector_name)
    collector_id = str(collector['id'])
    remove_sources(collector_id)

