#!/usr/bin/python --> 이거 민찬이가 환경에 적합한 형태로 변경해주세요
# -*- coding: utf-8 -*-

# Written by Ju Yeon Lee. justforher12344@gmail.com
# Co-worker: Min Chan Kim.

import re
import pandas as pd
import json
import requests
from file_transformer import FILE_TRANSFORMER

class EXPORT(Object):

    '''받은 데이터를 기반으로, AWS 클라우드 혹은 target 클라우드 주소에 파일을 생성하는 과정'''

    def __init__(self):
        text

    def _make_file(self, data):




    def to_front(self):

        ### front-end로 연결되는 특정 주소로 export 되게 할 것 ###


        from google.cloud import storage

        def upload_blob(bucket_name, source_file_name, destination_blob_name):
            """Uploads a file to the bucket."""
            # bucket_name = "your-bucket-name"
            # source_file_name = "local/path/to/file"
            # destination_blob_name = "storage-object-name"

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(source_file_name)

            print(
                "File {} uploaded to {}.".format(
                    source_file_name, destination_blob_name
                )
            )

        return

    def to_model(self):

        ### 이후 input 데이털ㄹ

        pass