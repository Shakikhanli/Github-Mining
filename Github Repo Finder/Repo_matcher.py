import json
from difflib import SequenceMatcher
from builtins import len, open

preferred_users = []
found_repos = []


def similar(repo1, repo2):
    return SequenceMatcher(None, repo1, repo2).ratio()


def front_back(front_list, back_list):
    matched_repos = []
    for front_repo in front_list:
        for back_repo in back_list:
            print(front_repo['repo_name'] + ' and ' + back_repo['repo_name'] + ' compared')
            if similar(front_repo['repo_name'], back_repo['repo_name']) > 0.5:
                matched_repos.append(front_repo['repo_name'] + '///' + back_repo['repo_name'])
    return matched_repos


with open('/Json files/' + 'Separated repos(2016-2017).json', 'r') as filehandle:
    file_content = json.load(filehandle)

for user in file_content:
    if len(user['front_list']) != 0 and len(user['back_list']) != 0:
        preferred_users.append(user)
print('All preferred users collected.')

count = 0
for each_user in preferred_users:
    if len(front_back(each_user['front_list'], each_user['back_list'])) == 0:
        print('No matches for user: ' + each_user['user_name'])
    else:
        count += 1
        found_repos.append(front_back(each_user['front_list'], each_user['back_list']))

# print(similar('happy-ionic-frontend', 'happy-express-backend'))
print('############################################################')
print(found_repos)
