# -*- coding:utf-8 -*-

"""program"""
__author__ = "Meritz RTX"
__date__ = "creation 2021-02-26"

# pip install tensorflow==2.4.0
# pip install gensim
# pip install scikit-learn
# pip install jupyter -> jupyter notebook --generate-config, notebook_dir 수정
# pip install nltk
# pip install pandas
# pip install matplotlib

import tensorflow as tf
import gensim
import sklearn
import nltk
import pandas as pd
import matplotlib as mpl

if __name__ == "__main__":

    print("tf.version :", tf.__version__)
    print("gensim.version :", gensim.__version__)
    print("sklearn.version :", sklearn.__version__)
    print("nltk.version :", nltk.__version__)
    # 아래 한번만 실행
    # nltk.download()
    print("pd.version :", pd.__version__)
    print("mpl.version :", mpl.__version__)
