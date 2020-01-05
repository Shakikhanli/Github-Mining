import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import time

# link = 'https://raw.githubusercontent.com/maddiereddy/Angular-NodeJS-MongoDB-CustomersService/master/src/package.json'
# page = requests.get(link)
# # file_content = page.json()
# # file_content.jsonloads()

user_name = 'cdoremus'
client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret

repo_list = []

first_link = 'https://api.github.com/users/' + user_name + '/repos?client_id=' + client_id \
             + '&client_secret=' + client_secret + '&per_page=45&page=1'
page = requests.get(first_link)
file_content = page.json()
repo_list.append(file_content)

while 'next' in page.links.keys():
    first_link = page.links['next']['url']
    print(first_link)
    page = requests.get(first_link)
    file_content = page.json()
    repo_list.append(file_content)

for each_page in repo_list:
    for each_repo in each_page:
        print(each_repo['name'])
