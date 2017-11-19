#!/usr/bin/env python3
#coding: utf-8
"""

Crawler https://hh.ru/

optional arguments:
  -h, --help        show this help message and exit
  -s SEARCH_STRING  Your find string
  -t TIME_OUT       Exit from time out in second
  -l PAGE_LIMIT     Limit pages view
  -v                Verbose mode on/off

actual date: november 2017

avedensky@gmail.com
"""
import requests
import sys
import csv
import sqlite3
from bs4 import BeautifulSoup
from time import time
from argparse import ArgumentParser


def parse_page_by_number(url, number):
    """
    Return list of dictionary with information about vacancy from one page on site
    """
    url += '&page='
    url += str(number)    

    response = requests.get(url, headers = {'user-agent': 'my-app/0.0.1'})
    if response.status_code != requests.codes.ok:
        print('Site Error, error code: {0}'.format(response.status_code))

    soup = BeautifulSoup(response.text, 'html.parser')
    finded_block = soup.find_all("div", class_="search-result-description")

    result = []

    for content in finded_block:
        info = {}

        title = content.find('a', class_=['search-result-item__name', 'search-result-item__name_ HH-LinkModifier'])
        info['title'] = title.string
        info['vacancy_url'] = title['href']

        salary = content.find('div', class_='b-vacancy-list-salary')
        info['salary'] = 'Не указано' if salary==None else salary.next.next.next 
        
        company = content.find('a', class_=['bloko-link','bloko-link_secondary'])
        info['company'] = 'Не указано' if company==None else company.string.strip()
        info['company_url'] = 'Не указано' if company==None else 'https://hh.ru'+company['href']

        address = content.find('span', attrs={"class": "searchresult__address", "data-qa":"vacancy-serp__vacancy-address"})
        info['address'] = 'Не указано' if address==None else address.next        

        metro = content.find('span', class_="metro-point")
        info['metro'] = 'Не указано' if metro==None else metro.next

        info['create_date'] = content.find('span', class_=['b-vacancy-list-date']).string

        short_description = content.find_all('div', class_=['search-result-item__snippet'])[0]         
        info['short_description'] = 'Не указано' if short_description==None else short_description.text                

        result.append(info)

    return result


def vacancy_search(searh_string, time_out=None, page_limit=None, verbose_mode=True):
    """
    searh_string - Your find string
    time_out - Exit from function by time out (second)
    page_limit - Max parse pages

    Return list of dictionary with information about all vacancy on site 
    """
    url =  r'https://hh.ru/search/vacancy'
    url += '?clusters=true&area=2&enable_snippets=true&text='
    url += searh_string

    result_lst = []
    page_number = 0
    store_time = time()
    while True:                
        if time_out!=None and time()-store_time >=time_out:
            break
        if page_limit!=None and page_number>=page_limit:
            break

        lst = parse_page_by_number(url, page_number)        
        page_number += 1

        if not lst: #empty
            break
        result_lst += lst
        if verbose_mode == True:
            print_info(lst)
            #print('{0} Cultivated:{1} page'.format(time(), page_number))

    return result_lst


def print_info(lst):
    """
    Print info to stdout
    """
    for i in lst:        
        for k,v in i.items():
            print('{0}: {1}'.format(k,v))
        print('-' * 50)


def save_to_csv(lst, filename):
    """
    Save parse info to csv file
    """
    with open(filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for i in lst:            
            spamwriter.writerow([value for value in i.values()])


def save_to_sqllite (lst, filename):
    """
    Save parse info to Data Base Sqlite
    """
    sql_table_create = '''CREATE TABLE IF NOT EXISTS hh (
                            id integer primary key AUTOINCREMENT,
                            title varchar(100) NOT NULL,
                            vacancy_url varchar(255) NOT NULL,
                            salary varchar(100) NOT NULL,
                            company varchar(100) NOT NULL,
                            company_url varchar(255) NOT NULL,
                            address varchar(100) NOT NULL,
                            metro varchar(100) NOT NULL,
                            create_date text NOT NULL,
                            short_description text NOT NULL
                            );'''

    sql_insert = '''INSERT INTO hh(
                    title, 
                    vacancy_url, 
                    salary, 
                    company, 
                    company_url, 
                    address,
                    metro, 
                    create_date, 
                    short_description
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    conn = sqlite3.connect(filename)    
    c = conn.cursor()    
    c.execute(sql_table_create)

    #insert
    for i in lst:        
        c.execute(sql_insert,[
            i['title'],
            i['vacancy_url'], 
            i['salary'], 
            i['company'], 
            i['company_url'], 
            i['address'],
            i['metro'],
            i['create_date'], 
            i['short_description']]
            )        

    conn.commit()
    conn.close()


def main():
    """
    Нажми на кнопку получишь результат... (из песни, гр. Технология)
    """        
    cmd_parser = ArgumentParser(description=
        'Crawler https://hh.ru/')

    cmd_parser.add_argument('-s', action='store', dest='search_string', 
        type=str, help='Your find string')

    cmd_parser.add_argument('-t', action='store', dest='time_out', 
        type=int, help='Exit from time out in second')

    cmd_parser.add_argument('-l', action='store', dest='page_limit', 
        type=int, help="Limit pages view")

    cmd_parser.add_argument('-csv', action='store', dest='csv_file_name', 
        type=str, help="Save to CSV file")

    cmd_parser.add_argument('-sqlite', action='store', dest='bd_file_name', 
        type=str, help="Save to SQLite BD")

    cmd_parser.add_argument('-v', action='store_true', dest='verbose', 
        help="Verbose mode on/off")

    args = cmd_parser.parse_args()
    if len(sys.argv)==1:
        cmd_parser.print_help()
        sys.exit(1)

    lst = vacancy_search(args.search_string, args.time_out, args.page_limit, args.verbose)

    # if args.verbose == True:     
    #     for i in lst:
    #         print ('{0:<55} {1:<20}'.format(i['title'][0:53], i['salary']))        

    if args.csv_file_name != None:
        save_to_csv(lst, args.csv_file_name)
                
    if args.bd_file_name != None:
        save_to_sqllite(lst, args.bd_file_name)        


if __name__=='__main__':
    main()

    