import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import time

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})


with open('/Json files/' + '(2017-01-01)---(2017-06-30).json', 'w') as file:
    json.dump(data, file)
