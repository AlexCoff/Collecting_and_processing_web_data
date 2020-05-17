
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
from pprint import pprint
vacancy_title = "Python"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept':'*/*'}
class hh_parser():

    def __init__(self):
        #some code
    
    def func_hh_parse(url):
        main_link = 'https://hh.ru'
        params = {'L_is_autosearch':'false',  \
                'area':2, \
                'text':vacancy_title, \
                'clusters':'true', \
                'enable_snippets':'true', \
                'page': 0 \
                }
        html = requests.get(main_link+'/search/vacancy',params=params,headers=header).text
        soup = bs(html,'lxml')
        vacancies_block = soup.find('div',{'class':'vacancy-serp'})
        vacancies_list = vacancies_block.findChildren('div',{'class':'vacancy-serp-item'},recursive=False)
        vacancies = []
        for vacancy in vacancies_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('div',{'class':'vacancy-serp-item__info'}).getText()
            vacancy_url = vacancy.find('div',{'class':'resume-search-item__info'}).find('a',{'class':'bloko-link'})['href']
            vacancy_source = main_link
            vacancy_salary_raw = vacancy.find('div',{'class':'vacancy-serp-item__sidebar'}).getText()


func_hh_list()    
func_hh_parse()
main_link = 'https://hh.ru'
params = {'quick_filters':'serials'}
html = requests.get(main_link+'/popular',params=params).text

soup = bs(html,'lxml')

serials_block = soup.find('div',{'class':'selection-list'})
serials_list = serials_block.findChildren(recursive=False)


serials = []
for serial in serials_list:
    serial_data = {}
    serial_link = main_link + serial.find('a',{'class':'selection-film-item-meta__link'})['href']
    serial_name = serial.find('p').getText()
    serial_genre = serial.find('span',{'class':'selection-film-item-meta__meta-additional-item'}).find_next_sibling().getText()
    serial_rating = serial.find('span',{'class':'rating__value'}).getText()

    serial_data['name'] = serial_name
    serial_data['link'] = serial_link
    serial_data['genre'] = serial_genre
    serial_data['rating'] = float(serial_rating)
    serials.append(serial_data)

pprint(serials)
