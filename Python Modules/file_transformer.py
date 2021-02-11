#!/usr/bin/python --> 이거 민찬이가 환경에 적합한 형태로 변경해주세요
# -*- coding: utf-8 -*-

# Written by Ju Yeon Lee. justforher12344@gmail.com
# Co-worker: Min Chan Kim.

import re
import pandas as pd
import json
import requests
import pymysql
from datetime import date, timedelta


class STT_transformer(object):

    '''To parse json file data from STT processing

    Example
    -------
    >>> import sys
    >>> sys.path.append('/home/hoheon/Packages/')
    >>> ## 사용방법

    >>> json_path = ## AWS에서 해당 위치 지정
    >>> 구체적 사용법 제시
    '''

    def __init__(self, json):
        assert type(json) is str, print('json path must be str.')

        self.path = json
        self.data = self._load_json()


    def _load_json(self):
        with open(self.path) as jsonfile:
            data = json.load(jsonfile)
        return data
