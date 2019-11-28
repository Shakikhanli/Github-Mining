import requests
import json
import pandas as pd
import pandas
from pandas.io.json import json_normalize
import os

commit_pages = []  # list of urls of commit pages
data = []
client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret
fail_list = []
stack_name = 'MERN stack'


def create_folder(username, projectname):
    path = '/Project folders/' + stack_name + '/' + username
    try:
        os.mkdir(path)
    except:
        print('')
    path = '/Project folders/' + stack_name + '/' + username + '/' + projectname
    try:
        os.mkdir(path)
    except:
        print('')


"""
Function to collect all commit pages
"""


def collect_page(repo_name, project_name):
    print("Processing of project " + project_name + " is started")
    collected_pages = []
    first_url = 'https://api.github.com/repos/' \
                + repo_name + '/' + project_name + '/commits?client_id=' \
                + client_id + '&client_secret=' + client_secret + '&per_page=45&page=1'
    res = requests.get(first_url)
    collected_pages.append(first_url)  # adding first url to our list
    while 'next' in res.links.keys():  # taking all url through pagination until it ends
        collected_pages.append(res.links['next']['url'])
        first_url = res.links['next']['url']
        res = requests.get(first_url)
    print(str(len(collected_pages)) + " pages are collected.")
    print(collected_pages)
    print("All commit pages are collected...")
    return collected_pages


"""
Function to collect all sha of all commits
"""


def collect_sha(pages):
    list_commit_sha = []
    list_commits = []
    for x in pages:
        page = requests.get(x)
        list_commits.append(page.json())
    print("amount of pages: " + str(len(list_commits)))
    for x in list_commits:  # here sha of each commit is taken
        for each_commit in x:
            try:
                list_commit_sha.append(each_commit['sha'])
            except:
                print("This commit has problem: " + x['message'])

    print("All commit sha collection is done ... ")
    print(" ")

    return list_commit_sha


"""
Function to create json strings.
"""


def collect_json_strings(list_commit_sha, repo_name, project_name, app_name, project_type):
    commit_counter = 0
    data = []
    for each_sha in range(len(list_commit_sha)):
        try:
            page2 = requests.get(
                'https://api.github.com/repos/' + repo_name + '/' + project_name + '/commits/' + list_commit_sha[
                    each_sha] + '?client_id=' + client_id + '&client_secret=' + client_secret)
            commit = page2.json()
            date = commit['commit']['author']['date']
            sha = commit['sha']
            commiter = commit['commit']['author']['name']
            commit_counter += 1
            commit_string = '{"date":"' + date + '","project_type":"' + project_type + \
                            '","commiter":"' + commiter + '","commit_id":"' + sha + '","files":['
        except:
            continue
        index = 0
        for each in commit['files']:
            index += 1
            try:
                commit_string = commit_string + '{"path":"' + each['filename'] + '","additions":"' + str(
                    each['additions']) + '","deletions":"' + str(each['deletions']) + '","changes":"' + str(
                    each['changes']) + '"}'
                if index < len(commit['files']):
                    commit_string = commit_string + ','
            except:
                continue
        commit_string = commit_string + ']}'
        print("Project name: " + project_name + ". " + str(len(list_commit_sha) - each_sha) + ' Commits lasted...')
        try:
            json_file = json.loads(commit_string)
            data.append(json_file)
        except:
            print("This commit has a problematic structure.")
            continue
        commit_string = ''
        print(' ')
    df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
    try:
        result = df.sort_values('date')
        create_folder(repo_name, app_name)
        Export = result.to_json(
            '/Project folders/' + stack_name + '/' + repo_name + '/' + app_name + '/' + project_name + r'.json')
        print("Processing of project: " + project_name + " is finished.")
        print(" ")
    except:
        print("Processing of project: " + project_name + " is FAILED !!!.")
        fail_list.append(repo_name + ' // ' + project_name)


df = pd.read_excel('Projects list.xlsx', sheet_name='MERN stack')
count = 0

for index, row in df.iterrows():

    front_links = '{"links":' + row['Frontend'] + '}'
    data = json.loads(front_links)
    for x in data['links']:
        commit_pages = collect_page(row['Repo_name'], x)
        sha_list = collect_sha(commit_pages)
        collect_json_strings(sha_list, row['Repo_name'], x, row['Project_name'], 'frontend')

    front_links = '{"links":' + row['Backend'] + '}'
    data = json.loads(front_links)
    for x in data['links']:
        commit_pages = collect_page(row['Repo_name'], x)
        sha_list = collect_sha(commit_pages)
        collect_json_strings(sha_list, row['Repo_name'], x, row['Project_name'], 'backend')

    print("PROJECT " + str(row['Project_name']) + " finished...")
