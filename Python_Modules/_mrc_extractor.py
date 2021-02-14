# Written by Ju Yeon Lee. justforher12344@gmail.com
# Co-worker: Min Chan Kim.

import re
import pandas as pd
import json
import requests
import pickles
from _file_transformer import FILE_TRANSFORMER

# 모델을 불러와서 활용 및 답을 내는 과정
# 사용되는 모든 모듈들 requirements.txt 로 정리하는 과정 필요

class FAQ_EXTRACTION(object):

    def __init__(self, type, path):
        self.path = path
        self.type = type
        self.question = _minutes_format()

        return

    def _read_file(self):

        return data

    def _minutes_format(self,type):

        # 포맷에 맞는 질의어를 리스팅하는 함수
        return

    def _model(self,type):

        # 회의록 타입마다 다른 모델이 필요할 경우를 대비

        return

    def answer(self, type):
        # 각 타입마다 추출되는 mrc 값들 확인
        pass


class QNA_EXTRACTION(object):
    def __init__(self):
        pass