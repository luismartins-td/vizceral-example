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
labelnames = sorted(labelnames)

data = {
  "renderer": "global",
  "name": "edge",
  "nodes": [{
    "renderer": "region",
    "name": "INTERNET",
    "class": "normal"
  }]
}

info = 0
warn = 0
danger = 0

clusters = {}
namespaces = []
requests = {}

for result in results:
    cluster = result['metric'].get("cluster_name", '')
    timestamp = result['value'][0]
    clusters[cluster]= timestamp
    namespace = result['metric'].get("exported_namespace", '')
    namespaces.append (namespace)
    request_val = result['value'][1]
    status_code = result['metric'].get("status", '')
    if int(status_code) >= 100 and int(status_code) < 400:
        if namespace+"-info" in requests.keys():
            requests[namespace+"-info"] += int(request_val)
            info += int(request_val)
        else:
            requests[namespace+"-info"] = int(request_val)
            info += int(request_val)
    elif int(status_code) >= 400 and int(status_code) < 500:
        if namespace+"-warn" in requests.keys():
            requests[namespace+"-warn"] += int(request_val)
            warn += int(request_val)
        else:
            requests[namespace+"-warn"] = int(request_val)
            warn += int(request_val)
    elif int(status_code) >= 500:
        if namespace+"-danger" in requests.keys():
            requests[namespace+"-danger"] += int(request_val)
            danger += int(request_val)
        else:
            requests[namespace+"-danger"] = int(request_val)
            danger += int(request_val)

namespaces_clear = list(set(namespaces))

for namespace in namespaces_clear:
    if namespace:
        if namespace+"-info" not in requests.keys():
            requests[namespace+"-info"] = 0
        if namespace+"-warn" not in requests.keys():
            requests[namespace+"-warn"] = 0
        if namespace+"-danger" not in requests.keys():
            requests[namespace+"-danger"] = 0

for cluster,timestamp in clusters.items():
    data["nodes"].append(
        {
            "renderer": "region",
            "name": cluster,
            "class": "normal",
            "maxVolume": 50000,
            "class": "normal",
            "updated": str(timestamp)
        }
    )
    data["nodes"][1].update({
        "nodes": [{
            "name": "INTERNET",
            "renderer": "focusedChild",
            "class": "normal"
        }]
    })
    for namespace in namespaces_clear:
        if namespace:
            data["nodes"][1]["nodes"].append({
                "name": namespace,
                "renderer": "focusedChild",
                "class": "normal"
            })
    data["nodes"][1].update({
        "connections": [{
        }]
    })
    for namespace in namespaces_clear:
        if namespace:
            data["nodes"][1]["connections"].append({
                "source": "INTERNET",
                "target": namespace,
                "metrics": {
                    "danger": str(requests[namespace+"-danger"]),
                    "normal": str(requests[namespace+"-info"]),
                    "warning": str(requests[namespace+"-warn"])
                },
                "class": "normal"
            })

data['connections'] = []
data['connections'].append({
    "source": "INTERNET",
    "target": "stg02",
    "metrics": {
    "normal": info,
    "warning": warn,
    "danger": danger
    },
    "notices": [
    ],
    "class": "normal"
})

#print (data)
with open('src/xxx.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)
