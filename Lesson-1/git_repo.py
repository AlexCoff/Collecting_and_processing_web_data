#! /usr/bin/env python
# -*- coding: utf-8 -*-
#1. Посмотреть документацию к API GitHub, разобраться как вывести список
#   репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json

main_link = 'https://api.github.com'
# user_name = "AlexCoff"
user_name = input('Please input username on GitHub: ')  # Ask username in console
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept':'*/*'}
response = requests.get(main_link + '/users/' + user_name + '/repos',headers=header)
if response.ok:
        data = json.loads(response.text)
        if len(data)==0:
                print(f"User {user_name} have not public repos")
        else:
                print(f"For user {user_name} list of public repository:")
                repo_data = []
                for i in range(0,len(data)):
                        repo = {}
                        repo['name'] = data[i]['name']
                        repo['url'] = data[i]['html_url']
                        repo['create_date'] = data[i]['created_at']
                        repo_data.append(repo)
                        print(data[i]['name'])
                #Write full data in file
                with open( './Lesson-1/full_data_to_user_' + user_name + '.json', 'w') as json_file:
                        json.dump(data, json_file)
                #Write only names, urls, create data
                with open( './Lesson-1/'+ user_name + '.json', 'w') as json_file:
                        json.dump(repo_data, json_file)

else:
        print('Incorrect input, or user not exist')