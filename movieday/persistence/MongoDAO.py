from pymongo import MongoClient
# MongoDB에 계정이 있거나 외부 IP인 경우
# DB_HOST = 'xxx.xx.xx.xxx:27017'
# DB_ID = 'root'
# DB_PW = 'pw'
# client = MongoClient('mongodb://%s:%s@%s' % (DB_ID, DB_PW, DB_HOST))
class MongoDAO:
    def __init__(self):
        # >> MongoDB Connection
        self.client = MongoClient('localhost', 27017) # 클래스 객체 할당
        self.db = self.client['local'] # MongoDB의 'local' DB를 할당
        self.collection = self.db.movie

    def mongo_write(self, data):
        print('>> MongoDB write data!')
        self.collection.insert(data)

    def mongo_update(self, data):
        pass

    def mongo_selectAll(self):
        pass

    def mongo_view(self, data):
        pass

    def mongo_delete(self, data):
        pass