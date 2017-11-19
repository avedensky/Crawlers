# Crawlers
<h3>
Демонстрационная программа парсинга сайтов, на примере сайта 
<a href="https://hh.ru/">Head Hunter</a>
</h3>

![Main Window](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/help_scr.png)

<br>
<a href="https://github.com/avedensky/crawlers/blob/master/hh.ru/hh_crawler.py">Посмотреть код</a>
<br>

<h3>Возможности программы:</h3>
<ul>
<li>
Сканирование информации о вакансиях
</li>
<li>
Выдача информации на экран (ключ -v)
</li>
<li>
Запись информации в файл csv (ключ -csv)
</li>
<li>
Запись информации в файл Базы Данных SQLite (ключ -sqlite)
</li>
<li>
Задать ограничение количества сканированных страниц (ключ -l)
</li>
<li>
Задать ограничение времени сканирования (ключ -t)
</li>
</ul>

<b>Примеры результатов работы программы:</b>
<br>
<br>
Информация на экран
![Verbose mode](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/verbose_scr.png)
<br>
Результат записанный в файл csv
![csv mode](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/csv_scr.png)
<br>
Результат записанный в файл Базы Данных SQLite
![BD mode](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/BD_scr.png)

<br>
<b>Примеры команд запуска программы:</b>
<br>
<br>
python3 ./hh_crawler.py -s программист -l 1 -v
<br>
<i>Просмотреть вакансии с ключевым словом программист, ограничиться сканированием 1 страницы, результат на экран</i>
<br>
<br>

python3 ./hh_crawler.py -s программист -csv s.csv -t 10
<br>
<i>Просмотреть вакансии с ключевым словом программист, ограничить время сканирования около 10 сек, результат в файл csv</i>
<br>
<br>

python3 ./hh_crawler.py -s программист -sqlite s.sqlite
<br>
<i>Просмотреть вакансии с ключевым словом программист, результат в файл Базы Данных SQLite (s.sqlite)</i>
<br>
