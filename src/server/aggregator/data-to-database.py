import datetime
import os
import json
import requests

path_len = len([name for name in os.listdir('data/') if os.path.isfile(os.path.join('data/', name))])
for i in range(path_len):
    this_date = str(datetime.date(2022, 11, 20) + datetime.timedelta(days=i))
    with open(f'data/offers-{this_date}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    response = requests.post(url='http://localhost:8080/insert-new-data', json=data)
    print((i + 1), this_date, response)
    
