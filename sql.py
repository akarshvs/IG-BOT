import sqlite3
import yaml
import pathlib
import os
from itertools import islice

conn = sqlite3.connect('./db.sqlite3')
c = conn.cursor() 

last_id = 17
c.execute('SELECT text FROM statement')

dict_file = []

user = 'akarsh'

dict_file.append(user)
for row in c.fetchall():
    dict_file.append(row[0])

with open(r'./convo_samples/{}.yml'.format(user), 'w') as file:
    yaml.dump(dict_file, file, explicit_start=True, default_flow_style=False)
