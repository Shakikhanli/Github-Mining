from builtins import len, open
from locale import str
import requests
import json
import pandas as pd
import time

client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret


def dict_creator(user_name, repo_list):
    df1 = pd.DataFrame(
        columns=['Name of repository', 'url', 'Frontend', 'Backend', 'Front/Backend', 'Angular', 'React',
                 'Vue', 'Ruby', 'TypeScript', 'JavaScript', 'Java', 'PHP', 'Python', 'MongoDB', 'MySql',
                 'PostgreSql'])

    for each_repo in repo_list:
        dict1 = {'Name of repository': '', 'url': '', 'Frontend': '', 'Backend': '', 'Front/Backend': '', 'Angular': '',
                 'React': '', 'Vue': '', 'Ruby': '', 'TypeScript': '', 'JavaScript': '', 'Java': '', 'PHP': '',
                 'Python': '', 'MongoDB': '', 'MySql': '', 'PostgreSql': ''}
        try:
            link = 'https://raw.githubusercontent.com/' + user_name + '/' + each_repo['repo_name'] + \
                   '/master/package.json?client_id=' + client_id + '&client_secret=' + client_secret
            page = requests.get(link)

            if page.status_code != 404:
                file_content = page.json()
                if "@angular/common" in file_content['dependencies']:
                    dict1['TypeScript'] = 'X'
                    dict1['Angular'] = 'X'
                elif "react" in file_content['dependencies']:
                    dict1['JavaScript'] = 'X'
                    dict1['React'] = 'X'
                else:
                    continue
                if dict1:
                    dict1['Frontend'] = 'X'
                    dict1['Name of repository'] = each_repo['repo_name']
                    dict1['url'] = 'https://api.github.com/repos/' + user_name + '/' + each_repo['repo_name']
                    series = pd.Series(dict1)
                    series.to_frame()
                    df1 = df1.append(series, ignore_index=True)


        except:
            continue
    return df1


data = pd.DataFrame(
    columns=['Name of repository', 'url', 'Frontend', 'Backend', 'Front/Backend', 'Angular', 'React',
             'Vue', 'Ruby', 'TypeScript', 'JavaScript', 'Java', 'PHP', 'Python', 'MongoDB', 'MySql',
             'PostgreSql'])

df = pd.DataFrame({'Name of repository': [], 'url': [], 'Frontend': [], 'Backend': [], 'Front/Backend': [],
                   'Angular': [], 'React': [], 'Vue': [], 'Ruby': [], 'TypeScript': [], 'JavaScript': [], 'Java': [],
                   'PHP': [], 'Python': [], 'MongoDB': [], 'MySql': [], 'PostgreSql': []})

with open('Json files/Separated repos((2017-01-01)---(2017-06-30).json') as json_file:
    users = json.load(json_file)

count = 0

for each_user in users:
    if len(each_user['front_list']) > 0:
        df = df.append(dict_creator(each_user['user_name'], each_user['front_list']))
        count += len(each_user['front_list'])
        print('Project of user ' + each_user['user_name'] + ' are ready. Added project count: ' + str(count))


writer = pd.ExcelWriter('data3.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1')
writer.save()

