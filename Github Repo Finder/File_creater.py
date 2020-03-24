from builtins import len, open
from locale import str
import requests
import json
import pandas as pd
import os.path
import time


client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret
id_secret = '?client_id=6ff8da2ae4d057a6d048&client_secret=3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'
data = []
links = []
loc = 'Database1.xlsx'
files = []
count = 0
save_path = 'C:/File Structure/'


def file_collecter(path):
    link = first_link + '/contents' + path + id_secret
    subpage = requests.get(link)
    subpage_content = subpage.json()

    for each_subfile in subpage_content:
        if each_subfile['type'] == 'file':
            files.append(each_subfile['path'])
        if each_subfile['type'] == 'dir':
            file_collecter(each_subfile['path'])


excel_data_df = pd.read_excel(loc, sheet_name='Sheet1')
json_str = excel_data_df.to_json(orient="records")

projects = json.loads(json_str)

for each_project in projects:
    try:
        first_link = each_project['url']
        page = requests.get(first_link + '/contents' + id_secret)
        if page.status_code == 404:
            print (first_link + '/contents' + id_secret)
        page_content = page.json()
        for each_file in page_content:
            if each_file['type'] == 'file':
                files.append(each_file['path'])
            if (each_file['type'] == 'dir') and (each_file['name'] != 'node_modules'):
                file_collecter(each_file['path'])
        print ('Collecting all lines are done.')
        count += 1
        completeName = os.path.join(save_path, each_project['Name of repository'] + ".txt")
        fh = open(completeName, 'w', encoding="utf-8")
        fh.writelines('\n'.join(files) + '\n')
        fh.close()
        print ('File succesfully created.')
        files = []
        print(each_project['Name of repository'] + ' is done. Projects left: ' + str(len(projects) - count) + '\n')
    except:
        print (first_link + '/contents' + id_secret)
    #     # print (first_link + '/contents' + id_secret)
    #     print (each_project['Name of repository'] + ' NOT WORKING !!!!!!!')
        time.sleep(65)
        continue