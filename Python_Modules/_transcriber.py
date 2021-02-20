import boto3
import json
import os
import time
from pathlib import Path
from urllib import request


class Transcriber:
    def __init__(self):
        self._init_s3()
        self._init_transcribe() 

    def _init_s3(self):
        self.s3 = boto3.resource('s3')
        s3_config = self._load_s3_config()
        self.bucket_name = s3_config['bucketName']
        self.s3_endpoint = s3_config['s3Endpoint']

    def _load_s3_config(self):
        config_file_dir = os.path.abspath(os.path.dirname(__file__))
        config_file_path = os.path.join(config_file_dir, 's3_config.json')
        config_file = open(config_file_path)
        s3_config = json.load(config_file)
        return s3_config

    def _init_transcribe(self):
        self.transcribe = boto3.client('transcribe')

    def upload(self, stream, filename):
        self.filename = filename
        self.s3.Bucket(self.bucket_name).upload_fileobj(stream, filename)

    def transcribe(self, num_speakers):
        job_name = self.filename
        format = Path(self.filename).suffix[1:]
        job_uri = (
            'https://' 
            + self.bucket_name
            + '.'
            + self.s3_endpoint
            + '/'
            + self.filename
        )
        self.transcribe.start_transcription_job(
            TranscriptionJobName = job_name,
            Media = {'MediaFileUri': job_uri},
            MediaFormat = format,
            LanguageCode = 'en-US',
            Settings = {
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': num_speakers
            }
        )
        result_in_json = self._wait_for_transcription_result(job_name)
        return result_in_json

    def _wait_for_transcription_result(self, job_name):
        status = None
        while True:
            status = self.transcribe.get_transcription_job(TranscriptionJobName = job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(5)
        result_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        result = request.urlopen(result_uri)
        result_in_json = result.read().decode('utf8')
        return result_in_json
