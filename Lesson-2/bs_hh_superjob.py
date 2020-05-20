
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
import re
import pandas as pd
#vacancy_title = "Python"

class parser():
    def __init__(self,vacancy_title): # init class
        self.__param_hh = {'L_is_autosearch':'false',  \
                'area':2, \
                'text':vacancy_title, \
                'clusters':'true', \
                'enable_snippets':'true', \
                'page': 0 \
                }
        self.__param_sj = {'keywords':vacancy_title, 'page': 1 }
        self.__header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept':'*/*'}
        self.__next_page_status = True
        self.__main_link_hh = 'https://hh.ru'
        self.__main_link_sj = 'https://spb.superjob.ru'
        self.__vac_list_hh = []
        self.__vac_list_sj = []
        self.__vac = []
        self.__next_page_url = ''

    def __check_next_page(self, p_block): # check if nex page button exist
        try:
            p_block.find('a',{'class':'HH-Pager-Controls-Next'})['href']
        except TypeError:
            self.__next_page_status = False
    def __check_next_page_sj(self, p_block): # check if nex page button exist

        try:
            self.__next_page_url = p_block.find('a',{'class':'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})['href']
        except TypeError:
            self.__next_page_status = False
    
    @staticmethod
    def __parse_salary(sal_raw):
        salar_dict = {}
        if re.search("договор",sal_raw):
            salar_dict['min'] = None
            salar_dict['max'] = None
            salar_dict['cur'] = None
        elif re.match('от',sal_raw):
            salar_dict['min'] = int(re.sub(r'\s+','',re.split(r'([а-я,А-Я,A-Z,a-z]+\.*\s*[а-я,А-Я,A-Z,a-z]*\.*)',sal_raw)[2]))
            salar_dict['max'] = None
            salar_dict['cur'] = re.split(r'([а-я,А-Я,A-Z,a-z]+\.*\s*[а-я,А-Я,A-Z,a-z]*\.*)',sal_raw)[3]
        elif re.match('до',sal_raw):
            salar_dict['min'] = None
            salar_dict['max'] = int(re.sub(r'\s+','',re.split(r'([а-я,А-Я,A-Z,a-z]+\.*\s*[а-я,А-Я,A-Z,a-z]*\.*)',sal_raw)[2]))
            salar_dict['cur'] = re.split(r'([а-я,А-Я,A-Z,a-z]+\.*\s*[а-я,А-Я,A-Z,a-z]*\.*)',sal_raw)[3]
        elif '-' in sal_raw:
            salar_dict['min'] = int(re.sub(r'\s+','',re.split('-',sal_raw)[0]))
            salar_dict['max'] = int(re.sub(r'\s+','',re.split(r'([а-я,А-Я,A-Z,a-z]+\.*\s*[а-я,А-Я,A-Z,a-z]*\.*)',re.split('-',sal_raw)[1])[0]))
            salar_dict['cur'] = re.split(r'([а-я,А-Я,A-Z,a-z]+\.*\s*[а-я,А-Я,A-Z,a-z]*\.*)',sal_raw)[1]
        else:
            salar_dict['min'] = None
            salar_dict['max'] = None
            salar_dict['cur'] = None
        return salar_dict
   
    
    @staticmethod
    def __vacancies_page_parse(self, vac_block): # create list of vacancy soup blocks

        vac_raw_list = vac_block.findChildren('div',{'class':'vacancy-serp-item'},recursive=False)
        for i in vac_raw_list:
            self.__vac_list_hh.append(i)
    @staticmethod
    def __vacancies_page_parse_sj(self, vac_block): # create list of vacancy soup blocks

        vac_raw_list = vac_block.findChildren('div',{'class':'iJCa5 f-test-vacancy-item _1fma_ _1JhPh _2gFpt _1znz6 _2nteL'},recursive=False)
        for i in vac_raw_list:
            self.__vac_list_sj.append(i)
    
    @staticmethod
    def __vacancy_parser(self):
        for vacancy in self.__vac_list_hh:
            vacancy_data = {}
            vacancy_name = vacancy.find('div',{'class':'vacancy-serp-item__info'}).getText()
            vacancy_url = self.__main_link_hh + vacancy.find('div',{'class':'vacancy-serp-item__info'}).find('a',{'class':'bloko-link'})['href']
            vacancy_source = self.__main_link_hh
            vacancy_salary_raw = vacancy.find('div',{'class':'vacancy-serp-item__sidebar'}).getText()
            salary_parsed = self.__parse_salary(vacancy_salary_raw)
            vacancy_data['name'] = vacancy_name
            vacancy_data['url'] = vacancy_url
            vacancy_data['source'] = vacancy_source
            vacancy_data['salary_raw'] = vacancy_salary_raw
            vacancy_data['salary_min'] = salary_parsed['min']
            vacancy_data['salary_max'] = salary_parsed['max']
            vacancy_data['salary_cur'] = salary_parsed['cur']
            self.__vac.append(vacancy_data)
    @staticmethod
    def __vacancy_parser_sj(self):
        for vacancy in self.__vac_list_sj:
            vacancy_data = {}
            vacancy_name = vacancy.find('div',{'class':'_3mfro'}).getText()
            vacancy_url = self.__main_link_sj + vacancy.find('div',{'class':'_3mfro'}).find('a')['href']
            vacancy_source = self.__main_link_sj
            vacancy_salary_raw = vacancy.find('span',{'class':'_3mfro'}).getText()
            salary_parsed = self.__parse_salary(vacancy_salary_raw)
            vacancy_data['name'] = vacancy_name
            vacancy_data['url'] = vacancy_url
            vacancy_data['source'] = vacancy_source
            vacancy_data['salary_raw'] = vacancy_salary_raw
            vacancy_data['salary_min'] = salary_parsed['min']
            vacancy_data['salary_max'] = salary_parsed['max']
            vacancy_data['salary_cur'] = salary_parsed['cur']

            self.__vac.append(vacancy_data)
    
    def parse_hh(self):
        self.__next_page_status = True
        while self.__next_page_status:
            #some code
            html = requests.get(self.__main_link_hh+'/search/vacancy',params=self.__param_hh,headers=self.__header).text
            cur_page = self.__param_hh['page']
            self.__param_hh['page'] += 1 
            soup = bs(html,'lxml')
            main_block = soup.find('div',{'class':'vacancy-serp-wrapper'}) # Select main block
            vacancies_block = main_block.find('div',{'class':'vacancy-serp'}) # Select only vacancy block
            pages_block = main_block.find('div',{'data-qa':'pager-block'})  # Select only block with page bar
            self.__vacancies_page_parse(self, vacancies_block)
            if pages_block:
                self.__check_next_page(pages_block)
                time.sleep(3) # wait 3 sec if next page block found
            else:
                self.__next_page_status = False
            print(f'Page {cur_page+1} parse complete hh') 

        self.__vacancy_parser(self) # parce vacancy

    def parse_sj(self):
        
        while self.__next_page_status:

            if self.__next_page_status:
                html = requests.get(self.__main_link_sj+'/vacancy/search',params=self.__param_sj,headers=self.__header).text
            else:
                html = requests.get(self.__main_link_sj+self.__next_page_url,headers=self.__header).text
           
            cur_page = self.__param_sj['page']
            self.__param_sj['page'] += 1
            
            soup = bs(html,'lxml')
            main_block = soup.find('div',{'class':'_1Ttd8 _2CsQi'}) # Select main block
            vacancies_block = main_block.find('div',{'class':'_1ID8B'}).find('div',{'style':'display:block'}) # Select only vacancy block
            pages_block = main_block.find('div',{'class':'_3zucV L1p51 undefined _2guZ- _GJem'})  # Select only block with page bar
            self.__vacancies_page_parse_sj(self, vacancies_block)
            self.__next_page_status = True
            if pages_block:
                self.__check_next_page_sj(main_block)
                time.sleep(3) # wait 3 sec if next page block found
            else:
                self.__next_page_status = False
            print(f'Page {cur_page} parse complete sj') 

        self.__vacancy_parser_sj(self) # parce vacancy    

    def vac_print(self):
        pprint(self.__vac)
    def get(self):
        return self.__vac

a=parser('Менеджер')

a.parse_sj()
a.parse_hh()
a.vac_print()
df = pd.DataFrame(a.get())

df.to_pickle('./Lesson-2/dump.pkl')


