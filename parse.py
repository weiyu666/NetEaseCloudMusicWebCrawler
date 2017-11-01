# -*-coding:utf-8 -*-
__author__ = 'my'

from utils import get_user_agent, get_tree, post
from encrypt import gen_data
import json
from store import Store
from random import choice
import threading
import time

follows_url = 'http://music.163.com/weapi/user/getfollows/{}?csrf_token='
playlist_url = 'http://music.163.com/weapi/user/playlist?csrf_token='
like_url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='

follow_urls = [127287036]
seen = set(follow_urls)


def get_follows(url, uid):
    text = {
        'username': 'username',
        'password': 'password',
        'rememberLogin': 'true',
        'uid': uid,
        'limit': '100'
        }
    data = gen_data(text)
    try:
        r = post(url.format(uid),data=data)
        users = r.json()['follow']
        for i in users:
            # print i['userId']
            if i['userId'] not in seen:
                seen.add(i['userId'])
                follow_urls.append(i['userId'])
    except:
        pass


def get_playlist(url, id):
    text = {
                "offset": '0',
                "uid": id,
                "limit": '100',
                # "csrf_token": csrf
            }
    data = gen_data(text)
    try:
        r = post(url.format(id),data=data)
        # return r
        return r.json()['playlist'][0]['id']
    except:
        pass


def get_likemusic(url, id, uid):
    music_id = []
    text = {
          'id': id,
        'limit': '1000',
        'totla': 'True',
        'n': '1000',
        'offset': '0'
    }
    data = gen_data(text)
    try:
        r = post(url.format(id), data=data)
        # print json.loads(r.text)['playlist']['trackIds']
        music_ids = json.loads(r.text)['playlist']['trackIds']
        for i in music_ids:
            # print i
            music_id.append(i['id'])
        store = Store()
        store.setitem(uid, music_id)
    except:
        pass

def process():
    while True:
        try:
            # uid = choice(follow_urls)
            # get_follows(follows_url, uid)
            get_likemusic(like_url, id=get_playlist(playlist_url, uid), uid=uid)
            time.sleep(3)
        except IndexError:

            break
       
threads = []
while threads or follow_urls:
    for thread in threads:
        if not thread.is_alive():
            threads.remove(thread)
    while len(threads) < 10 and follow_urls:
        uid = choice(follow_urls)
        get_follows(follows_url, uid)
        thread = threading.Thread(target=process)
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
    time.sleep(3)

