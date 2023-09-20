


import json
import requests

url = "http://127.0.0.1:5000/wins/1"#http://<host>/wins/<username>
headers = {'Content-type': 'application/json'}
data = {'username': '1'}
r = requests.post(url, data=json.dumps(data), headers=headers)


