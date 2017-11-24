# hh_crawler
<h3>
Parsing demonstration program, for site:
<a href="https://hh.ru/">Head Hunter</a>
</h3>

![Main Window](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/help_scr.png)

<br>
<a href="https://github.com/avedensky/crawlers/blob/master/hh.ru/hh_crawler.py">Code view</a>
<br>

<h3>Capabilities</h3>
<ul>
<li>
Scan job vacancy information on site
</li>
<li>
Show finded information (key -v)
</li>
<li>
Record to file in csv format(key -csv)
</li>
<li>
Record data to base SQLite (as file) (key -sqlite)
</li>
<li>
Set pages scan limit (key -l)
</li>
<li>
Set timeout of scan (key -t)
</li>
</ul>

<b>Example of result:</b>
<br>
<br>
Show to screen
![Verbose mode](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/verbose_scr.png)
<br>
Data to csv format
![csv mode](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/csv_scr.png)
<br>
Data to data base SQLite
![BD mode](https://github.com/avedensky/crawlers/raw/master/hh.ru/img/BD_scr.png)

<br>
<b>Example console comand:</b>
<br>
<br>
python3 ./hh_crawler.py -s manager -l 1 -v
<br>
<i>Scan job vacancy like as 'manager', scan limit one page, show to screen</i>
<br>
<br>

python3 ./hh_crawler.py -s manager -csv s.csv -t 10
<br>
<i>Scan job vacancy like as 'manager', time out scan at 10 scecond, store to file s.csv</i>
<br>
<br>

python3 ./hh_crawler.py -s manager -sqlite s.sqlite
<br>
<i>Scan job vacancy like as 'manager', data to SQLite (s.sqlite)</i>
<br>
