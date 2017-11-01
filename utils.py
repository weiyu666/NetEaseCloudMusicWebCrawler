# -*- coding:utf-8 -*-
__author__ = 'my'




import random

import requests
from lxml import etree
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from encrypt import gen_data
# from config import PROXIES

proxy_list = []
def get_proxy():
    proxys = requests.get('http://127.0.0.1:8000/?types=0&protocol=0&count=10&country=%E4%B8%AD%E5%9B%BD')
    ip_ports = json.loads(proxys.text)
    for ip in ip_ports:
        # ip_ports = json.loads(proxys.text)
        proxy_list.append(ip[0] + ':' + str(ip[1]))
    return random.choice(proxy_list)
proxies = {'http': 'http://' + get_proxy()}
print proxies

TIMEOUT = 5


def get_user_agent():
    ua = UserAgent()
    # print ua.random
    return ua.random


def fetch(url, retry=0):
    s = requests.Session()
    # proxies = {
    #     'http': choice_proxy()
    # }
    s.headers.update({'user-agent': get_user_agent(),
                      'referer': 'http://music.163.com/'})
    try:
        return s.get(url, timeout=TIMEOUT, proxies=proxies)
    except requests.exceptions.ConnectionError:
        if retry < 3:
            return fetch(url, retry=retry + 1)
        raise


def post(url, data):
    headers = {
        'Host': 'music.163.com',
        'Connection': 'keep-alive',
        'Content-Length': '500',
        'Origin': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'http://music.163.com/user/follows?id=127287036',
        'Accept-Encoding': 'gzip, deflate',
    }

    return requests.post(url, headers=headers, data=data,proxies=proxies, timeout=5)


def get_tree(url):
    r = fetch(url)
    return BeautifulSoup(r.text, 'lxml')


print get_user_agent()
