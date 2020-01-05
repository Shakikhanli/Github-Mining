from builtins import len, open
from locale import str
import requests
import json
import pandas as pd
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
    files = []
    first_link = 'https://api.github.com/users/' + user_name + '/repos?client_id=' + client_id \
                 + '&client_secret=' + client_secret + '&per_page=45&page=1'
    page = requests.get(first_link)
    file_content = page.json()
    files.append(file_content)
    while 'next' in page.links.keys():
        first_link = page.links['next']['url']
        page = requests.get(first_link)
        file_content = page.json()
        files.append(file_content)
    for each_page in files:
        for each_repo in each_page:
            repo_list.append(each_repo['name'])
    return repo_list


def json_designer(front_list, back_list, other_list, user_name):
    index = 0
    json_line = '{"user_name":"' + user_name + '", "user_url":"' + 'https://github.com/' + user_name + \
                '", "front_list":['
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
            if page.status_code == 404:
                link = 'https://raw.githubusercontent.com/' + user_name + '/' + y + \
                       '/master/src/package.json?client_id=' + client_id + '&client_secret=' + client_secret
                page = requests.get(link)
            file_content = page.json()
            if "@angular/common" in file_content['dependencies']:
                front_list.append(y)
                # print('FRONT')
            elif "react" in file_content['dependencies']:
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
        if (len(json_file['front_list']) > 0) and (len(json_file['back_list']) > 0):
            data.append(json_file)
        json_string = ''
        print(str(count) + ' users checked.')
    except:
        print("API ratio exceed. Application will sleep 65 seconds...")
        time.sleep(65)
        continue

with open('/Json files/' + 'Separated repos(2016---2017).json', 'w') as file:
    json.dump(data, file)
