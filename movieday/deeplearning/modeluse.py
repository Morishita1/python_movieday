import tensorflow as tf
import numpy as np
from konlpy.tag import Okt
from pymongo import MongoClient
from pprint import pprint

# MongoDB Connection
client = MongoClient('localhost', 27017) # ip주소, port번호
db = client['local'] # 'local' Database 선택
# collection = db.movie # Collection 선택
collection = db.get_collection('movie') # 동적으로 Collection 선택

# MongoDB 데이터 불러오기
reply_list = [] # MongoDB Document를 담을 List
for one in collection.find({},{'_id':0,'cont':1}):
    reply_list.append(one['cont']) # dict에서 Value만 추출
# print('>> 댓글내용')
# pprint(reply_list)
# print('count', len(reply_list))

# Okt() 형태소 분석기 객체 생성
okt = Okt()

# selectword.txt 불러오기
def read_data(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        data = []
        while True:
            line = f.readline()[:-1]
            if not line: break
            data.append(line)
    return data

select_words = read_data('selectword.txt')
# print(select_words[:10])

# 모델 불러오기
model = tf.keras.models.load_model('my_model.h5')


def tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]


def term_frequency(doc):
    return [doc.count(word) for word in select_words]


# 예측하는 함수 구현
def predict_pos_neg(review):
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        print('[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다:)'.format(review, score*100))
    else:
        print('[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다:)'.format(review, (1-score)*100))


# 예측시작
for one in reply_list:
    predict_pos_neg(one)




