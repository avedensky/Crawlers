#!/usr/bin/env python3
#coding: utf-8
"""
Базовый класс парсера
"""
from global_defines import *
from glossary import Glossary
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
import requests
import re
import pickle
import time
from datetime import datetime


log = logging.getLogger(__name__)

class ParserBase:
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self._data_output = None
        self._glossary = None

    @property
    def data_output(self):
        return self._data_output

    @property
    def header_key_list(self):
        return self._header_key_list

    @property
    def order_key_list(self):
        return self._order_key_list        

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class TestOnlyParser(ParserBase):    
    def __init__(self):
        super().__init__()
        self._data_output = [
                {'title':'Notebook', 'price':1000, 'mark':'asus'}, 
                {'title':'Notebook', 'price':2000, 'mark':'toshiba'},
                {'title':'Notebook', 'price':2500, 'mark':'sony'},
                {'title':'HDD 6Gb', 'price':100, 'mark':'seagete'}, 
                {'title':'HDD 8Gb', 'price':200, 'mark':'toshiba'},
                {'title':'HDD 10Gb', 'price':300, 'mark':'western digital'},
        ]         
    def run(self):
        pass


class KinozalParser(ParserBase):
    def __init__(self):
        super().__init__()
        self._page_time_sleep = 1
        self._detail_page_time_sleep = 0.500
        self._start_page_number = 0
        self._page_limit = 20        
        self._glossary = Glossary()
        self._data_output = []
        self._url = 'https://kinozal-tv.appspot.com/'
        self._request_header = {'user-agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0', 'Charset': 'utf-8'}

    @property
    def url(self):
        return self._url

    def __login(self):
        s = requests.Session()
       
        r = s.post('https://kinozal-tv.appspot.com/takelogin.php', {
             'username': '',
             'password': '',
             'remember': 0,
        }, headers = request_header)

    def __logout(self):
        r = requests.get(self._url, headers = self._request_header)
        if r.status_code != requests.codes.ok:
            log.error('Site Error, error code: {0}'.format(r.status_code))

        soup = BeautifulSoup (r.text, 'html.parser')
        b = soup.find('a', href=re.compile('logout.php'))

        r = s.get(self._url+b['href'], headers = self._request_header)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self._data_output, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self._data_output = pickle.load(f)
      
    def __parse_desc1_3(self, text, out_voc):
        """
        """
        text = text.replace('\t','')
        text = text.replace('Выставлен',', Выставлен')
        lines = text.split('\n')        
        for line in lines:
            for num, key in enumerate(self._glossary.search_keys):
                if line.startswith(key):  
                    store_key = self._glossary.store_keys[num]                  
                    out_voc[store_key] = line.replace(key+':','').lstrip()

    def _parse_page_detail(self, url, out_voc):
        """
        """
        r = requests.get(url, headers = self._request_header)
        if r.status_code != requests.codes.ok:
             log.error('Site Error, error code: {0}'.format(r.status_code))        

        soup = BeautifulSoup(r.text, 'html.parser')
        ul_block = soup.find('ul', class_=['men w200'])

        #Get Statistic
        href_list = ul_block.find_all('a')
        for href in href_list:
            lines = href.text.split('\n')
            for line in lines:
                for num, key in enumerate(self._glossary.search_keys):
                    if line.startswith(key):
                        store_key = self._glossary.store_keys[num]
                        out_voc[store_key] = line.replace(key,'').strip()

        out_voc['rating'] = ul_block.find('span', itemprop='ratingValue').text
        out_voc['voices'] =  ul_block.find('span', itemprop='votes').text

        block_justify = soup.find_all('div', class_=['bx1 justify'])
        for i in block_justify:
            if i.find('p'):
                out_voc['about'] = i.p.text[i.p.text.find(':')+1:].strip('')

        time.sleep(self._detail_page_time_sleep)
 
    def _parse_page_main(self, number):
        """
        """
        u = self._url
        u +='?page='
        u += str(number)
        r = requests.get(u, headers = self._request_header)
        if r.status_code != requests.codes.ok:
            log.error('Site Error, error code: {0}'.format(r.status_code))

        soup  = BeautifulSoup(r.text, 'html.parser')
        film_info_blocks = soup.find_all('div', class_='tp1_body')        
        
        for i in film_info_blocks:
            v = {}
            el = i.find('a')            
            v['title'] = el['title']
            v['parse_datetime'] = str(datetime.now())
            v['detail_url'] = self._url+el['href']

            el = i.find('img', class_='tp1_img')
            v['img_url'] = el['src']

            el = i.find('div', class_='tp1_desc1')
            self.__parse_desc1_3(el.text, v)

            el = i.find('div', class_='tp1_desc2')
            v['about'] = el.text.split(':')[1]

            el = i.find('div', class_='tp1_desc3')
            self.__parse_desc1_3(el.text, v)

            #get detail info            
            self._parse_page_detail(v['detail_url'], v)            

            self._data_output.append(v)

        
    def run(self):
        page_count = self._start_page_number
        while True:
            log.info('Culivate page: {}'.format(page_count))
            if page_count>=self._start_page_number+self._page_limit:
                break                
            self._parse_page_main(page_count)
            page_count +=1
            time.sleep(self._page_time_sleep)
