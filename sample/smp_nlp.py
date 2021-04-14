# -*- coding:utf-8 -*-

"""program"""
__author__ = "Meritz RTX"
__date__ = "creation 2021-02-26"


from konlpy.utils import pprint
from konlpy.tag import Kkma
from konlpy.tag import Okt
from konlpy.tag import Mecab

test_str = "쿠팡배달 메리츠화재와 어린이보험과 긴급출동 삼성생명이 펫퍼민트 고객에 대한 보장성 보험 위험률 사망율 감사 수술위험 이벤트 보장합니다."



def okt_test():
    okt = Okt()
    # print(okt.morphs(test_str))
    print(okt.nouns(test_str))
    # print(okt.pos(test_str))



def main():
    print("--------------------------------------------------------")
    okt_test()


if __name__ == "__main__":
    main()
