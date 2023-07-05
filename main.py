import ntpath
import os
import sys
import textwrap
from urllib.parse import urlparse

import requests
import yaml

from SiteParser import SiteParser

ARTICLE = 'article'
CLASS = 'class'
CONTENT = 'content'
DIVS = 'divs'
ITEMPROP = 'itemprop'
TAG = 'tag'
TITLE = 'title'
CONFIG_FILE_NAME = 'config.yml'


def init_site_parser(parser: SiteParser, site_name: str):
    escaped_site_name = site_name.replace(".", "_")
    with open(CONFIG_FILE_NAME, "r") as stream:
        config = yaml.safe_load(stream)
        if not escaped_site_name in config:
            print(
                'В файле конфигурации {} не найден шаблон {} для сайта {}.'.format(CONFIG_FILE_NAME, escaped_site_name,
                                                                                   site_name))
            sys.exit(1)
        site_config = config[escaped_site_name]

        article_site_config = site_config[ARTICLE]
        parser.article_tag = article_site_config[TAG]
        if CLASS in article_site_config:
            parser.article_class = article_site_config[CLASS]
        elif ITEMPROP in article_site_config:
            parser.article_itemprop = article_site_config[ITEMPROP]

        title_site_config = site_config[TITLE]
        parser.title_tag = title_site_config[TAG]
        if CLASS in title_site_config:
            parser.title_class = title_site_config[CLASS]
        elif ITEMPROP in title_site_config:
            parser.title_itemprop = title_site_config[ITEMPROP]

        content_site_config = site_config[CONTENT]
        parser.content_tag = content_site_config[TAG]
        parser.content_divs = content_site_config[DIVS]
        if CLASS in content_site_config:
            parser.content_class = content_site_config[CLASS]
        elif ITEMPROP in content_site_config:
            parser.content_itemprop = content_site_config[ITEMPROP]


def save_to_file_by_url(url, data):
    path, file_name = ntpath.split(url.path)
    if file_name:
        file_name = file_name.rpartition('.')[0] + '.txt'
    else:
        file_name = 'index.txt'
    path = url.netloc + path
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, file_name)
    with open(file_path, "w") as f:
        f.write(data)
    print('Текст статьи сохранен в файл {}.'.format(file_path))


if len(sys.argv) != 2:
    print('В параметрах запуска приложения необходимо указать адрес статьи, которую необходимо сохранить в файл.')
    sys.exit(1)

if not os.path.exists(CONFIG_FILE_NAME):
    print('Для запуска приложения необходим конфигурационный файл config.yml.')
    sys.exit(1)

url_param = sys.argv[1]
response = requests.get(url_param)
response.raise_for_status()
url = urlparse(url_param)

parser = SiteParser(response.text)
init_site_parser(parser, url.netloc)
save_to_file_by_url(url, parser.parse())
