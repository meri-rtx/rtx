# -*- coding:utf-8 -*-
import pandas as pd
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle

okt = Okt()
max_len = 30


def load_stopwords():
    fp = open("../resource/stopwords_kor.txt", "r", encoding='UTF8')
    lines = fp.readlines()
    fp.close()
    df = pd.DataFrame(columns=["words", "pos", "prob"])
    i = 0
    for line in lines:
        # print(line.strip().split('\t'))
        df.loc[i] = line.strip().split('\t')
        i += 1

    # print(type(df['words'].tolist()))

    return df, df['words'].tolist()


def load_token():
    fp = open("../resource/news/new_token.dat", "rb")
    data = pickle.load(fp)
    fp.close()

    return data


# Read File
def read_file():
    fp = open("../data/data_test.txt", "r", encoding='UTF8')
    lines = fp.readlines()
    fp.close()

    return lines


# Filtering
def sentiment_predict(new_sentence):
    new_sentence = okt.morphs(new_sentence, stem=True)  # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords]  # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩
    score = float(loaded_model.predict(pad_new))  # 예측
    if score > 0.5:
        print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
        return 1, 0
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
        return 0, 1


def predict_file(lines):
    gv, nv = 0, 0
    for line in lines:
        line = line.replace("[^ㄱ-ㅎㅏ-ㅣ가-힝 ]","")
        if len(line.strip()) < 3: continue
        print(line)
        gvt, nvt = sentiment_predict(line)
        gv += gvt
        nv += nvt

    return gv, nv


def main():
    print("1. 일단 파일 읽자")
    lines = read_file()
    print("2. Filtering/Transform/Cleaning")
    gv, nv = predict_file(lines)
    if gv > nv:
        print("긍정 :", gv, nv)
    elif gv == nv:
        print("중립 :", gv, nv)
    else:
        print("부정 :", gv, nv)


if __name__ == "__main__":
    df_sw, stopwords = load_stopwords()
    tokenizer = load_token()
    loaded_model = load_model("../resource/news/best_model.h5")
    #main()

    sentiment_predict('이 영화 핵노잼 ㅠㅠ')
    sentiment_predict('이 영화 너무 추천합니다,')
    sentiment_predict('이 영화 추천하지 않습니다.')
    sentiment_predict('이 영화 감동으로 눈물이 납니다.')
