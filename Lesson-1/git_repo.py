#! /usr/bin/env python
# -*- coding: utf-8 -*-
#1. Посмотреть документацию к API GitHub, разобраться как вывести список
#   репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json

main_link = 'https://api.github.com'
# user_name = "AlexCoff"
user_name = input('Please input username on GitHub: ')  # из файла
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept':'*/*'}
response = requests.get(main_link + '/users/' + user_name + '/repos',headers=header)
if response.ok:
    data = json.loads(response.text)
    if len(data)==0:
        print(f"User {user_name} have not public repos")
    else:
        print(f"For user {user_name} list of public repository:")
        for i in range(0,len(data)):
                print(data[i]['name'])
else:
        print('Incorrect input, or user not exist')
