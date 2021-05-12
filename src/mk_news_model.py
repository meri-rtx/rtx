import pandas as pd
import numpy as np
import urllib.request
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

DEBUG = True
okt = Okt()
stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']


def load_data():
    urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt",
                               filename="ratings_train.txt")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt",
                               filename="ratings_test.txt")

    return pd.read_table('ratings_train.txt'), pd.read_table('ratings_test.txt')


def cleaning_data():
    global train_data, test_data
    train_data.drop_duplicates(subset=['document'], inplace=True)  # document 열에서 중복인 내용이 있다면 중복 제거
    train_data = train_data.dropna(how='any')  # Null 값이 존재하는 행 제거
    train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
    train_data['document'] = train_data['document'].str.replace('^ +', "")  # white space 데이터를 empty value로 변경
    train_data['document'].replace('', np.nan, inplace=True)
    train_data = train_data.dropna(how='any')

    test_data.drop_duplicates(subset=['document'], inplace=True)  # document 열에서 중복인 내용이 있다면 중복 제거
    test_data = test_data.dropna(how='any')  # Null 값이 존재하는 행 제거
    test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")  # 정규 표현식 수행
    test_data['document'] = test_data['document'].str.replace('^ +', "")  # 공백은 empty 값으로 변경
    test_data['document'].replace('', np.nan, inplace=True)  # 공백은 Null 값으로 변경
    test_data = test_data.dropna(how='any')  # Null 값 제거


def tokenize_data():
    X_train = []
    for sentence in train_data['document']:
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        X_train.append(temp_X)

    X_test = []
    for sentence in test_data['document']:
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        X_test.append(temp_X)

    return X_train, X_test


def encoding_data():
    global X_train, X_test
    global vocab_size
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)
    # 1차 
    threshold = 3
    total_cnt = len(tokenizer.word_index)  # 단어의 수
    rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if (value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    vocab_size = total_cnt - rare_cnt + 1

    tokenizer = Tokenizer(vocab_size)
    tokenizer.fit_on_texts(X_train)
    # 2차
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)

    return X_train, X_test, tokenizer


def post_processing():
    global X_train, y_train, X_test, y_test
    drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
    # 빈 샘플들을 제거
    X_train = np.delete(X_train, drop_train, axis=0)
    y_train = np.delete(y_train, drop_train, axis=0)

    drop_test = [index for index, sentence in enumerate(X_test) if len(sentence) < 1]
    # 빈 샘플들을 제거
    X_test = np.delete(X_test, drop_test, axis=0)
    y_test = np.delete(y_test, drop_test, axis=0)

    X_train = pad_sequences(X_train, maxlen=max_len)
    X_test = pad_sequences(X_test, maxlen=max_len)


def make_model():
    model = Sequential()
    model.add(Embedding(vocab_size, 100))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)

    return load_model('best_model.h5')


def sentiment_predict(new_sentence):
    new_sentence = okt.morphs(new_sentence, stem=True)  # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩
    score = float(loaded_model.predict(pad_new))  # 예측
    if (score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))


if __name__ == "__main__":
    train_data, test_data = load_data()

    cleaning_data()

    X_train, X_test = tokenize_data()

    vocab_size = 0
    X_train, X_test, tokenizer = encoding_data()

    y_train = np.array(train_data['label'])
    y_test = np.array(test_data['label'])
    max_len = 30
    post_processing()

    loaded_model = make_model()

    sentiment_predict('이 영화 핵노잼 ㅠㅠ')
    sentiment_predict('이 영화 너무 추천합니다,')
