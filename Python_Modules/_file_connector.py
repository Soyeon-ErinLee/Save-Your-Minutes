#!/usr/bin/python --> 이거 민찬이가 환경에 적합한 형태로 변경해주세요
# -*- coding: utf-8 -*-

# Written by Ju Yeon Lee. justforher12344@gmail.com
# Written by Min Chan Kim.
# 가능하다면 다른 모듈에 합치기 가능

import re
import pandas as pd
import json
import requests
from _file_transformer import SttTransformer
from _transcriber import Transcriber

'''
path1 = audio file path 

Transcriber()
SttTransformer()

path2 = text file path 

flask 

'''


class Connector():

    def __init__(self):
        self.path = file


    def make_file(self, path):

        assert type(path) is str, print("text input must be string.")

        file = open(path, 'w')  # hello.txt 파일을 쓰기 모드(w)로 열기. 파일 객체 반환
        file.write(html_string)  # 파일에 문자열 저장
        file.close()
        pass



def to_front(self):

    ### front-end로 연결되는 특정 주소로 export 되게 할 것 ###


    return

def to_model(self):

    ### 이후 input 데이털ㄹ

    pass