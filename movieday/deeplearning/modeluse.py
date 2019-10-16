import tensorflow as tf
import numpy as np
from konlpy.tag import Okt

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


predict_pos_neg('올해 최고의 영화! 세 번 넘게 봐도 질리지가 않네요')
predict_pos_neg('배경 음악이 영화의 분위기랑 너무 안 맞습니다. 몰입에 방해가 됨니다. ')
predict_pos_neg('재미는 있는데 시간떼우기용이네요...')