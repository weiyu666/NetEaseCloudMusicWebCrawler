# -*-coding:utf-8 -*-


from pymongo import MongoClient , errors


class Store:
    def __init__(self, client=None):
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.collection
        # self.music = self.db.music


    # def __getitem__(self, uid):
    #     record = self.music.find_one({'_id': uid})
    #     if record:
    #         return record['result']
    #     else:
    #         raise KeyError(uid + 'does not exist')

    def setitem(self, uid, result):
        record = {'musicid':result}
        self.db.music.update({'_id': uid}, {'$set': record}, upsert=True)
