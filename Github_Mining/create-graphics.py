import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd

fail_list = []


def pie_chart(category1, category2, value1, value2, name):
    slices_files = [value1, value2]
    activities = [category1, category2]
    colors = ['r', 'g']
    plt.pie(slices_files, labels=activities, colors=colors, startangle=90, autopct='%.1f%%')
    plt.savefig("/Project folders/" + 'Graphics/' + name + '_commit_history.png')
    plt.clf()


def bar_graph(repo_name, name, bar_count, value_list1, value_list2):
    N = bar_count
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    p1 = plt.bar(ind, value_list1, width)
    p2 = plt.bar(ind, value_list2, width, bottom=value_list1)
    plt.ylabel('Shares of FrontEnd and BackEnd according to the timeline')
    plt.title('Percentages of FrontEnd and BackEnd. Project:' + name)
    plt.yticks(np.arange(0, 0.1, 1))
    plt.legend((p1[0], p2[0]), ('FrontEnd', 'BackEnd'))
    print(name)
    plt.savefig("/Project folders/" + 'Graphics/' + name + '_commit_history.png')
    plt.clf()


# Here it all rows in current excel sheet to the df data frame
df = pd.read_excel('Projects list.xlsx', sheet_name='MEAN stack')
count = 0

for index, row in df.iterrows():
    min_date = '2100-02-21 00:00:00'
    max_date = '2001-02-21 00:00:00'
    FMT = '%Y-%m-%d %H:%M:%S'
    commit_counter = 0
    date_increment = 0
    percentagesOfFE = []
    percentagesOfBE = []
    files_column = []
    reponame = row['Repo_name']
    projectname = row['Project_name']
    front_changes = 0
    back_changes = 0

    # Here all combined json files in current folder are checked and graphic created accoridng to the commits
    try:
        df1 = pd.read_json(
            'Project folders/' + 'MEAN stack/' + row['Repo_name'] + '/' + row['Project_name'] + '/' + row[
                'Project_name'] + '_(Combined).json')
    except:
        continue

    column_dates = df1['date'][0:len(df1['date'])]
    df1 = df1.sort_values(by=['date'])
    for x in column_dates:
        if str(x) < min_date:
            min_date = str(x)
        if str(x) > max_date:
            max_date = str(x)

    tdelta = datetime.strptime(max_date, FMT) - datetime.strptime(min_date, FMT)
    if tdelta < timedelta(days=101):
        date_increment = 5
    if (tdelta > timedelta(days=101)) and (tdelta < timedelta(days=501)):
        date_increment = 15
    if (tdelta > timedelta(days=500)) and (tdelta < timedelta(days=1501)):
        date_increment = 50
    if (tdelta > timedelta(days=1500)) and (tdelta < timedelta(days=2500)):
        date_increment = 75
    if (tdelta > timedelta(days=2500)) and (tdelta < timedelta(days=4000)):
        date_increment = 200

    min_date = datetime.strptime(str(min_date), FMT) + timedelta(days=date_increment)
    alfa = min_date

    numOfChangesInFrontEnd = 0
    numOfChangesInBackEnd = 0

    print("min: " + str(min_date))
    print("max: " + str(max_date))
    print("delta: " + str(tdelta))

    for index, row in df1.iterrows():
        if row['date'] < datetime.strptime(str(min_date), FMT):
            if row['project_type'] == 'frontend':
                files_column = row['files']
                for z in files_column:
                    numOfChangesInFrontEnd += int(z['changes'])
                    front_changes += int(z['changes'])
            else:
                files_column = row['files']
                for z in files_column:
                    numOfChangesInBackEnd += int(z['changes'])
                    back_changes += int(z['changes'])
        else:
            min_date = datetime.strptime(str(min_date), FMT) + timedelta(days=date_increment)
            commit_counter += 1
            sumOfModifiedLines = numOfChangesInFrontEnd + numOfChangesInBackEnd
            if sumOfModifiedLines == 0:
                percentagesOfFE.append(sumOfModifiedLines)
                percentagesOfBE.append(sumOfModifiedLines)
            else:
                percentagesOfFE.append(numOfChangesInFrontEnd / sumOfModifiedLines)
                percentagesOfBE.append(numOfChangesInBackEnd / sumOfModifiedLines)
            numOfChangesInFrontEnd = 0
            numOfChangesInBackEnd = 0

    print('commit_counter: ' + str(commit_counter))
    # print('Percantage FE: ' + str(percentagesOfFE))
    # print('Percentage BE: ' + str(percentagesOfBE))
    print('Front-end changes: ' + str(front_changes))
    print('Back-end changes: ' + str(back_changes))
    try:
        # bar_graph(reponame,projectname,commit_counter, percentagesOfFE, percentagesOfBE)
        pie_chart('front_changes', 'back_changes', front_changes, back_changes, projectname)
        front_changes = 0
        back_changes = 0
        print('Graphic of ' + projectname + ' is ready!')
    except:
        fail_list.append(reponame + '_' + projectname)
