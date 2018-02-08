#!/usr/bin/env python3
#coding: utf-8

"""
Этот модуль служит для запуска парсера (точка входа - main())
"""

from global_defines import *
import sys
import os.path
from argparse import ArgumentParser
from customparser import *
from out import OutToConsole, OutToCSV, OutToExcel, OutToSQLite, OutToJSON

log =  logging.getLogger(__name__)

def main():    
    ap = ArgumentParser(description='Crawler/Parser site/documents Version 0.0.1')
    ap.add_argument('-con', action='store_true', dest='out_console',help="Print to console (stdout)")
    ap.add_argument('-csv', action='store', dest='csv_file_name', type=str, help="Save to CSV file")
    ap.add_argument('-hcsv', action='store_true', dest='csv_show_header', help="Show header as first row for csv")
    ap.add_argument('-excel', action='store', dest='xls_file_name', type=str, help="Save to Excel file format")
    ap.add_argument('-hxls', action='store_true', dest='xls_show_header', help="Show header as first row in excel file")
    ap.add_argument('-sqlite', action='store', dest='sqlite_file_name', type=str, help="Save data to SQLite data base")
    ap.add_argument('-json', action='store', dest='json_file_name', type=str, help="Save to JSON file format")

    args = ap.parse_args()
    if len(sys.argv)==1:
        ap.print_help()
        sys.exit(0)

    #parser = TestOnlyParser()    
    parser = KinozalParser()    
    parser.run()
    parser.save('data.dat')
    #parser.load('data.dat')    

    if parser.data_output == None:
        log.error('Parsed data is empty!')
        exit()

    if args.out_console:
        out_console = OutToConsole()
        out_console.run(parser=parser)

    if args.csv_file_name:
        out_csv = OutToCSV()
        out_csv.run(parser=parser, filename=args.csv_file_name, header=args.csv_show_header)

    if args.xls_file_name:
        out_xls = OutToExcel()
        out_xls.run(parser=parser, filename=args.xls_file_name, header=args.xls_show_header)

    if args.sqlite_file_name:
        out_sqlite = OutToSQLite()
        out_sqlite.run(parser=parser, filename=args.sqlite_file_name)

    if args.json_file_name:
        out_json = OutToJSON()
        out_json.run(parser=parser, filename=args.json_file_name)        


if __name__ == '__main__':
    main()



