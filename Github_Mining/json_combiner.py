import requests
import json
import pandas as pd
import pandas
from pandas.io.json import json_normalize
import os

list_commit_sha = []  # list to save sha of commit
commit_pages = []  # list of urls of commit pages
data = []
client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret
fail_list = []
stack_name = 'MEAN stack'


def create_folder(username, appname):
    path = '/Project folders/' + stack_name + '/' + username
    try:
        os.mkdir(path)
    except:
        print('')
    path = '/Project folders/' + stack_name + '/' + username + '/' + appname
    try:
        os.mkdir(path)
    except:
        print('')


df = pd.read_excel('Projects list.xlsx', sheet_name=stack_name)
count = 0

for index, row in df.iterrows():
    min_date = '2100-02-21 00:00:00'
    max_date = '2001-02-21 00:00:00'
    FMT = '%Y-%m-%d %H:%M:%S'
    file_counter = 0

    try:
        path_to_json = 'Project folders/' + stack_name + '/' + row['Repo_name'] + '/' + row['Project_name']
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        files = []
        for x in json_files:
            df1 = pd.read_json(
                'Project folders/' + stack_name + '/' + row['Repo_name'] + '/' + row['Project_name'] + '/' + str(x))
            files.append(df1)
            df = pandas.concat(files, axis=0, ignore_index=True)
            df.reset_index()
            df = df.sort_values(by=['date'])

            Export = df.to_json(
                'Project folders/' + stack_name + '/' + row['Repo_name'] + '/' + row['Project_name'] + '/' + row[
                    'Project_name'] + '_(Combined)' + r'.json')
        count += 1
        print("Commit files of " + row['Project_name'] + " combined... " + str(count) + ' combined')
        print(' ')
    except:
        print(row['Repo_name'] + ' not founded...')
        fail_list.append(row['Repo_name'] + '_' + row['Project_name'])
