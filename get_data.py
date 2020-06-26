#!/usr/local/bin/python

import requests
import sys
import json

if len(sys.argv) != 3:
    print('Usage: {0} http://prometheus:9090 a_query'.format(sys.argv[0]))
    sys.exit(1)

response = requests.get('{0}/api/v1/query'.format(sys.argv[1]),
        params={'query': sys.argv[2]})
results = response.json()['data']['result']

# Build a list of all labelnames used.
labelnames = set()
for result in results:
      labelnames.update(result['metric'].keys())

# Canonicalize
labelnames.discard('__name__')
labelnames = sorted(labelnames)

data = {
  "renderer": "global",
  "name": "edge",
}
data['nodes'] = []
data['nodes'].append({
    "renderer": "region",
    "name": "INTERNET",
    "class": "normal"
})

info = 0
warn = 0
danger = 0

clusters = {}
namespaces = set()
requests = {}

for result in results:
    cluster = result['metric'].get("cluster_name", '')
    timestamp = result['value'][0]
    clusters[cluster]= timestamp
    namespace = result['metric'].get("exported_namespace", '')
    namespaces.add (namespace)
    requests[namespace+"_info"] = 1233
    requests[namespace+"_warn"] = 324523423
    requests[namespace+"_danger"] = 123213


    # requests = result['value'][1]
    # status_code = result['metric'].get("status", '')
    # if status_code >= 100 and status_code < 400
    #     info += requests = result['value'][1]
    # elif status_code >= 400 and status_code < 500
    #     warn += requests = result['value'][1]
    # elif status_code >= 500
    #     danger += requests = result['value'][1]

for cluster,timestamp in clusters.items():
    append = '"renderer": "region","name": "'+cluster+'","maxVolume": 50000,"class": "normal","updated":'+str(timestamp)+',"nodes": ['
    for namespace in namespaces:
        if namespace:
            append += '{"name": "INTERNET","renderer": "focusedChild","class": "normal"},{"name": '+namespace+',"renderer": "focusedChild","class": "normal"},'
    append += '],"connections": ['
    for namespace in namespaces:
        if namespace:
            append += '{"source": "INTERNET","target": '+namespace+',"metrics": {"danger": 116.524,"normal": 15598.906},"class": "normal"},'
    append += ']'
    print (append)

data['nodes'].append({
    append
})

# for cluster in clusters:
#     data['nodes'].append({
#         "renderer": "region",
#         "name": cluster,
#         "maxVolume": 50000,
#         "class": "normal",
#         "updated": namespaces[cluster+"_timestamp"],
#         "nodes": [
#         {
#           "name": "INTERNET",
#           "renderer": "focusedChild",
#           "class": "normal"
#         },
#         {
#           "name": namespace,
#           "renderer": "focusedChild",
#           "class": "normal"
#         }
#         ],
#         "connections": [
#         {
#           "source": "INTERNET",
#           "target": namespace,
#           "metrics": {
#             "danger": 116.524,
#             "normal": 15598.906
#           },
#           "class": "normal"
#         }
#         ]
#     })

# data['connections'] = []
# data['connections'].append({
#     "source": "INTERNET",
#     "target": "stg02",
#     "metrics": {
#     "normal": 26037.626,
#     "danger": 92.37
#     },
#     "notices": [
#     ],
#     "class": "normal"
# })


#     l = [result['metric'].get('__name__', '')] + result['value']
#     for label in labelnames:
#         l.append(result['metric'].get(label, ''))
#     print (result['metric'].get("exported_namespace", ''))
#     print (str(result['metric'].get("exported_namespace", '')) + str(result['value']))


# with open('src/xxx.json', 'w') as outfile:
#     json.dump(data, outfile, indent=2)
