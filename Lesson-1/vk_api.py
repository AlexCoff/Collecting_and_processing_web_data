#! /usr/bin/env python
# -*- coding: utf-8 -*-
#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
import requests
import json

main_link = 'https://api.vk.com'
method = '/method/users.getFollowers'
user_id= 19656918
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept':'*/*'}
param = {'user_id':user_id,'v':'5.103','access_token':'5337aac15337aac15337aac128534652ac553375337aac10d884bc050308aca73d35d55'}
response = requests.get(main_link + method,headers=header,params=param)
if response.ok:
        data = json.loads(response.text)
        with open( './Lesson-1/vk'+ str(user_id) + '.json', 'w') as json_file:
            json.dump(data, json_file)

else:
        print('Incorrect input, or user id not exist')