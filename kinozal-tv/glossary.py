#!/usr/bin/env python3
#coding: utf-8
"""
Базовый класс парсера
"""

class Glossary:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Реальные индентификаторы используемые программой
        self._store_keys =  (
                                'title',
                                'parse_datetime',
                                'detail_url',
                                'img_url', 
                                'avtor', 
                                'original_title', 
                                'create_year', 
                                'genre', 
                                'producer', 
                                'director', 
                                'actors', 
                                'about', 
                                'quality', 
                                'video', 
                                'audio', 
                                'size', 
                                'duration', 
                                'translate',
                                'distribute',
                                'download',
                                'downloaded',
                                'file_list',
                                'comments',
                                'imdb_rating',
                                'kinopoisk_rating',
                                'rating',
                                'voices'

        )

        #Индентификаторы которые используются для дополнительного поиска при разборе текста
        self._search_keys =  (
                                'Название',
                                'Дата время парсинга',
                                'url',
                                'img_url', 
                                'Автор', 
                                'Оригинальное название', 
                                'Год выпуска', 
                                'Жанр', 
                                'Выпущено', 
                                'Режиссер', 
                                'В ролях', 
                                'Описание', 
                                'Качество', 
                                'Видео', 
                                'Аудио', 
                                'Размер', 
                                'Продолжительность', 
                                'Перевод',
                                'Раздают',
                                'Скачивают',
                                'Скачали',
                                'Список файлов',
                                'Комментариев',
                                'IMDb',
                                'Кинопоиск',
                                'Рэйтинг',
                                'Голосов'

        )

        #То что будет выводиться в заголовке, например таблиц
        self._header_keys = (
                                'Название',
                                'Дата время парсинга',
                                'url',
                                'img_url', 
                                'Автор', 
                                'Оригинальное название', 
                                'Год выпуска', 
                                'Жанр', 
                                'Производство', 
                                'Режиссер', 
                                'В ролях', 
                                'Описание', 
                                'Качество', 
                                'Видео', 
                                'Аудио', 
                                'Размер', 
                                'Продолжительность', 
                                'Перевод',
                                'Раздают',
                                'Скачивают',
                                'Скачали',
                                'Список файлов',
                                'Комментариев',
                                'IMDB рэйтинг',
                                'Кинопоиск рэйтинг',
                                'Рэйтинг',
                                'Голосов'

        )

        #Порядок сортировки
        self._ordered_keys = (
                                'title',
                                'parse_datetime',
                                'detail_url',
                                'img_url', 
                                'avtor', 
                                'original_title', 
                                'create_year', 
                                'genre', 
                                'producer', 
                                'director', 
                                'actors', 
                                'about', 
                                'quality', 
                                'video', 
                                'audio', 
                                'size', 
                                'duration', 
                                'translate',
                                'distribute',
                                'download',
                                'downloaded',
                                'file_list',
                                'comments',
                                'imdb_rating',
                                'kinopoisk_rating',
                                'rating',
                                'voices'
        )

        self._sql_create_table = '''
                                CREATE TABLE IF NOT EXISTS films (
                                id integer primary key AUTOINCREMENT,
                                title text,
                                parse_datetime text,
                                detail_url text,
                                img_url text,
                                avtor text,
                                original_title text,
                                create_year numeric,
                                genre text, 
                                producer text,
                                director text,
                                actors text,
                                about text,
                                quality text,
                                video text,
                                audio text,
                                size text,
                                duration text,
                                translate text,
                                distribute integer,
                                download integer,
                                downloaded integer,
                                file_list text,
                                comments text,
                                imdb_rating real,
                                kinopoisk_rating real,
                                rating real,
                                voices integer                                
        );       
        '''

        self._sql_index_by_title = '''
                                CREATE UNIQUE INDEX IF NOT EXISTS MyUniqueIndexTitle ON films (title);
        '''

        self._sql_insert = '''
                                INSERT OR IGNORE INTO films(                                
                                title,
                                parse_datetime,
                                detail_url,
                                img_url, 
                                avtor, 
                                original_title, 
                                create_year, 
                                genre, 
                                producer, 
                                director, 
                                actors, 
                                about, 
                                quality, 
                                video, 
                                audio, 
                                size, 
                                duration, 
                                translate,
                                distribute,
                                download,
                                downloaded,
                                file_list,
                                comments,
                                imdb_rating,
                                kinopoisk_rating,
                                rating,
                                voices
                                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        
    @property
    def store_keys(self):
        return self._store_keys

    @property
    def search_keys(self):
        return self._search_keys

    @property
    def header_keys(self):
        return self._header_keys

    @property
    def ordered_keys(self):
        return self._ordered_keys        

    @property
    def sql_create_table(self):
        return self._sql_create_table

    @property
    def sql_insert(self):
        return self._sql_insert 

    @property
    def sql_index_by_title(self):
        return self._sql_index_by_title 
