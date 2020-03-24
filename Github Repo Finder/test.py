from builtins import len, open
from locale import str
import requests
import xlrd
import json
import pandas as pd
import time
import os

client_id = '6ff8da2ae4d057a6d048'  # you have to write your own id
client_secret = '3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'  # you have to write your own secret
id_secret = '?client_id=6ff8da2ae4d057a6d048&client_secret=3b6868e71ae5ef6d14a5d8114a3638e84bc22c7a'

fh = open('hello.txt','w')

lines_of_text = ['One line of text here', 'and another line here', 'and yet another here', 'and so on and so forth']

fh.writelines('\n'.join(lines_of_text) + '\n')

fh.close()
