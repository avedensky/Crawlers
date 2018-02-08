# #!/usr/bin/env python3
# #coding: utf-8
# """
# Глобальные определения для всего проекта парсера

# Отладчик (Для использования установаить: pip3 install pudb)
#     Запуск отладчика: python -m pudb.run
#     Установить break point, в коде: bp()
# """
import logging
import sys

#log_format_str = u'%(asctime)s %(filename)s[%(lineno)4d] %(levelname)-8s | %(message)s'
log_format_str = u'%(message)s'
logging.basicConfig(format = log_format_str, level = logging.INFO)

def bp(): #set break point for pubd (debuger)
    from pudb import set_trace; set_trace()

def save_text(f, text):
    with open(f,'w+') as file:
        file.write(text)


# with open('level1.html', 'r') as file:
        #     data = file.read()             
        # soup = BeautifulSoup(data, 'html.parser')

                # with open('level1.html','w') as file:
        #     file.write(response.text)


        # with open('res'+str(number)+'.html','w') as file:
        #     file.write(response.text)
        # return            

        # with open('res.html', 'r') as file:
        #     data = file.read()

        # with open('res.html','w') as file:
        #     file.write(response.text)
