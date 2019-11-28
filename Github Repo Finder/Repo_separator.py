import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import time

client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret
all_name = []
data = []
file_name = 'frontend_typescript_(MEAN)repos'

"""
DEFINITIONS!!!   collect_repo collects all repositories of certain user and returns it as list. 
"""


def collect_repo(user_name):
    repo_list = []
    link = 'https://api.github.com/users/' + user_name + '/repos?client_id=' + client_id \
           + '&client_secret=' + client_secret
    page = requests.get(link)
    file_content = page.json()
    for x in file_content:
        repo_list.append(x['name'])
    return repo_list


def json_designer(front_list, back_list, other_list, user_name):
    index = 0
    json_line = '{"user_name":"' + user_name + '", "front_list":['
    for x in front_list:
        index += 1
        json_line = json_line + '{"repo_name":"' + x + '"}'
        if index < len(front_list):
            json_line = json_line + ','
    json_line = json_line + '], "back_list":['
    index = 0

    for x in back_list:
        index += 1
        json_line = json_line + '{"repo_name":"' + x + '"}'
        if index < len(back_list):
            json_line = json_line + ','
    json_line = json_line + '], "other_list":['
    index = 0

    for x in other_list:
        index += 1
        json_line = json_line + '{"repo_name":"' + x + '"}'
        if index < len(other_list):
            json_line = json_line + ','
    json_line = json_line + ']}'

    print(json_line)
    return json_line


def sort_repo(user_name, repo_names):
    index = 0
    front_list = []
    back_list = []
    other_list = []
    for y in repo_names:
        index += 1
        try:
            link = 'https://raw.githubusercontent.com/' + user_name + '/' + y + \
                   '/master/package.json?client_id=' + client_id + '&client_secret=' + client_secret
            page = requests.get(link)
            file_content = page.json()
            if "@angular/common" in file_content['dependencies']:
                front_list.append(y)
                # print('FRONT')
            elif "express" in file_content['dependencies']:
                back_list.append(y)
                # print('BACK')
            elif "mongoose" in file_content['dependencies']:
                back_list.append(y)
                # print('BACK')
            else:
                other_list.append(y)
                # print('OTHERS')
        except:
            other_list.append(y)
            continue
        # print(str(len(repo_names) - index) + ' projects last ...')
    # json_designer(front_list, back_list, other_list, user_name)
    print(' ')
    return json_designer(front_list, back_list, other_list, user_name)


df1 = pd.read_json('Json files/2016---2017.json')
column_names = df1['owner_name'][0:len(df1['owner_name'])]

count = 0
print('Processing starts')
for each_name in column_names:
    count += 1
    try:
        json_string = sort_repo(each_name, collect_repo(each_name))
        json_file = json.loads(json_string)
        data.append(json_file)
        json_string = ''
        print(str(count) + ' users checked.')
    except:
        print("API ratio exceed. Application will sleep 65 second...")
        time.sleep(65)
        continue

with open('/Json files/' + 'Separated repos(2016-2017).json', 'w') as file:
    json.dump(data, file)

