#!/usr/bin/env python3
#coding: utf-8
"""
"""
from global_defines import *
from glossary import Glossary
from abc import ABCMeta, abstractmethod, abstractproperty
import csv
import xlwt
import sqlite3
import json
log =  logging.getLogger(__name__)

class OutBase:
    """ Abstract base class
    """    
    __metaclass__= ABCMeta

    def __init__(self, *args, **kwargs):
        self._data_input = None
        self._console_arg = kwargs.get('console_argumet_parser')
        self._glossary = None      
    
    @property
    def data_input(self):
        raise AttributeError # only for record       

    @data_input.setter
    def data_input(self, value):
        self._data_input = value

    @abstractmethod    
    def run(*args, **kwargs):
        pass        


class OutToConsole(OutBase):
    """Show data to console (stdout)
    """    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self._glossary = Glossary()                   
    
    def run(self, *args, **kwargs):
        """ Вывод на консоль
        """
        if not 'parser' in kwargs:
            log.error('no parser')
            return

        for item in kwargs['parser'].data_output:
            for j, key in enumerate(self._glossary.ordered_keys):
                if key in item:           
                    print ('{:<22} : {:<57}'.format(self._glossary.header_keys[j], item[key]))
            print ('-'*79)

    def __str__(self):
        return 'Show to Console'


class OutToCSV(OutBase):
    """Export to CSV file format
    """ 
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self._glossary = Glossary()
        self._delimiter = ';'
    

    def run(self, *args, **kwargs):
        """ Сохранение в CSV файл
        """
        log.info('\n--- Export to CSV file ---')
        log.info("Saving data to CSV file: '{}' wait ...".format(kwargs['filename']))

        if not 'parser' in kwargs:
            log.error('no parser')
            return

        with open(kwargs['filename'], 'w') as file:
            data_writer = csv.writer(file, delimiter=self._delimiter)

            if kwargs.get('header', False) == True:
                data_writer.writerow(self._glossary.header_keys)
                      
            for item in kwargs['parser'].data_output:                
                data_writer.writerow([item.get(key,'') for key in self._glossary.ordered_keys])

        log.info("File '{}' successfully recorded".format(kwargs['filename']))
        log.info('-'*30)

    def __str__(self):
        return 'Export to CSV'


class OutToExcel(OutBase):
    """Export to Excel file format
    """
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        self._glossary = Glossary()

    def run(self, *args, **kwargs):
        """ Сохранение в XLS файл
        """
        log.info('\n--- Export to Excel file ---')
        log.info("Saving data to Excel file: '{}' wait ...".format(kwargs['filename']))

        if not 'parser' in kwargs:
            log.error('no parser')
            return
       
        wb = xlwt.Workbook()
        ws0 = wb.add_sheet('Parsed data')

        #print title
        if kwargs.get('header', False) == True:                
            for col, title in enumerate(self._glossary.header_keys):
                ws0.write(0, col, title)                

        #print data
        for row, item in enumerate(kwargs['parser'].data_output):
            for col, key in enumerate(self._glossary.ordered_keys):                
                ws0.write(row+1, col, item.get(key, ''))

        wb.save(kwargs['filename'])              
        log.info("File '{}' successfully recorded".format(kwargs['filename']))
        log.info('-'*30)

    def __str__(self):
        return 'Export to Excel (xls format)'


class OutToSQLite(OutBase):
    """Export to SQLite file data base
    """
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        self._glossary = Glossary()       

    def _create_table(self, cursor):
        log.info("Creating table...")
        cursor.execute(self._glossary.sql_create_table)

    def _no_duplicate_by_title(self, cursor):
        log.info("Set 'do not duplicate (by title)', when insert")
        cursor.execute(self._glossary.sql_index_by_title)

    def _insert_data(self, cursor, data_output):
        log.info("Insert data...")
        for item in data_output:
            cursor.execute(self._glossary.sql_insert, [item.get(key, '') for key in self._glossary.ordered_keys])

    def run(self, *args, **kwargs):
        """ Сохранение в sqllite data base
        """
        log.info('\n--- Export to SQLite data base file ---')

        if not 'parser' in kwargs:
            log.error('no parser')
            return

        with sqlite3.connect(kwargs['filename']) as conn:        
            cursor = conn.cursor()
            self._create_table(cursor)
            self._no_duplicate_by_title(cursor)
            self._insert_data(cursor, kwargs['parser'].data_output)
            conn.commit()            

        log.info("File '{}' successfully recorded".format(kwargs['filename']))
        log.info('-'*30)

    def __str__(self):
        return 'Export to SQLite data base'      


class OutToJSON(OutBase):
    """Export to JSON file format
    """ 
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)                

    def run(self, *args, **kwargs):
        """ Сохранение в JSON файл
        """
        log.info('\n--- Export to JSON file format---')
        log.info("Saving data to JSON file format: '{}' wait ...".format(kwargs['filename']))

        if not 'parser' in kwargs:
            log.error('no parser')
            return

        with open(kwargs['filename'], 'w') as file:
            json.dump(kwargs['parser'].data_output, file)            

        log.info("File '{}' successfully recorded".format(kwargs['filename']))
        log.info('-'*30)

    def __str__(self):
        return 'Export to JSON'                       
