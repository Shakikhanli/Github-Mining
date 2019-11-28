


import boto3

s3 = boto3.client('s3')

s3.upload_file('2016---2017.json', 'githubmining1', 'first_data.json')


