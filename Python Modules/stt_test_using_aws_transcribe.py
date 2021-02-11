import boto3
import time
from urllib import request

transcribe = boto3.client('transcribe')

job_name = 'stt_test'
job_uri = 'https://s3_endpoint/filename'

transcribe.start_transcription_job(
    TranscriptionJobName = job_name,
    Media = {'MediaFileUri': job_uri},
    MediaFormat = 'mp3',
    MediaSampleRateHertz = 44100,
    LanguageCode = 'en-US',
    Settings = {
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 2
    }
)

status = None
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName = job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(5)

print(status)

result_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

load = request.urlopen(result_uri)
result = load.read().decode('utf8')
file = open('result.txt', 'w')
file.write(result)
file.close()

