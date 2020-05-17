
#1) Необходимо собрать информацию о вакансиях на вводимую должность 
# (используем input или через аргументы) с сайта superjob.ru и hh.ru. 
# Приложение должно анализировать несколько страниц сайта(также вводим 
# через input или аргументы). Получившийся список должен содержать в себе минимум:
#
#*Наименование вакансии
#*Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
#*Ссылку на саму вакансию
#*Сайт откуда собрана вакансия

#По своему желанию можно добавить еще работодателя и расположение. 
# Данная структура должна быть одинаковая для вакансий с обоих сайтов. 
# Общий результат можно вывести с помощью dataFrame через pandas.
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlparse, parse_qs
from pprint import pprint
import time
#vacancy_title = "Python"

class hh_parser():
    def __init__(self,vacancy_title): # init class
        self.__param = {'L_is_autosearch':'false',  \
                'area':2, \
                'text':vacancy_title, \
                'clusters':'true', \
                'enable_snippets':'true', \
                'page': 0 \
                }
        self.__header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept':'*/*'}
        self.__next_page_status = True
        self.__main_link = 'https://hh.ru'
        self.__vac_list = []
        self.__vac = []

    def __check_next_page(self, p_block): # check if nex page button exist
        try:
            p_block.find('a',{'class':'HH-Pager-Controls-Next'})['href']
        except TypeError:
            self.__next_page_status = False

    
    @staticmethod
    def __vacancies_page_parse(self, vac_block): # create list of vacancy soup blocks

        vac_raw_list = vac_block.findChildren('div',{'class':'vacancy-serp-item'},recursive=False)
        for i in vac_raw_list:
            self.__vac_list.append(i)
    
    
    def parse(self):
        while self.__next_page_status:
            #some code
            html = requests.get(self.__main_link+'/search/vacancy',params=self.__param,headers=self.__header).text
            cur_page = self.__param['page']
            self.__param['page'] += 1 
            soup = bs(html,'lxml')
            main_block = soup.find('div',{'class':'vacancy-serp-wrapper'}) # Select main block
            vacancies_block = main_block.find('div',{'class':'vacancy-serp'}) # Select only vacancy block
            pages_block = main_block.find('div',{'data-qa':'pager-block'})  # Select only block with page bar
            self.__vacancies_page_parse(self, vacancies_block)
            if pages_block:
                self.__check_next_page(pages_block)
                time.sleep(10) # wait 10 sec if next page block found
            else:
                self.__next_page_status = False
            print(f'Page {cur_page} parse complete') 

        self.__vacancy_parser(self) # parce vacancy

    def vac_print(self):
        pprint(self.__vac)

    @staticmethod    
    def __vacancy_parser(self):
        for vacancy in self.__vac_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('div',{'class':'vacancy-serp-item__info'}).getText()
            vacancy_url = vacancy.find('div',{'class':'vacancy-serp-item__info'}).find('a',{'class':'bloko-link'})['href']
            vacancy_source = self.__main_link
            vacancy_salary_raw = vacancy.find('div',{'class':'vacancy-serp-item__sidebar'}).getText()
            vacancy_data['name'] = vacancy_name
            vacancy_data['url'] = vacancy_url
            vacancy_data['source'] = vacancy_source
            vacancy_data['salary_raw'] = vacancy_salary_raw
            self.__vac.append(vacancy_data)

a=hh_parser('Системный архитектор')

a.parse()
a.vac_print()