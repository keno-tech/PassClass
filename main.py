import boto3
from urllib.request import urlopen
import json

session = boto3.Session(
    aws_access_key_id='AKIATCKAOOBQCFQWP25S',
    aws_secret_access_key='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'
)

def transcribe_video(bucket_name, object_key, language_code='en-US'):
    transcribe = session.client('transcribe', region_name='ap-southeast-2')

    job_name = "job"

    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat='mp3',
        Media={
            'MediaFileUri': f's3://{bucket_name}/{object_key}'
        }
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcription_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        transcription_result = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print("Transcription successful. Transcript file URI:", transcription_result)
        return transcription_file_uri

    else:
        print("Transcription failed.")


def extract_text(filename):
    response = urlopen(filename)
    data = json.loads(response.read())
    print(data["results"]["transcripts"][0]['transcript'])

bucket_name = "videos-lecture-helper"
object_key = "COMP30024_2024_SM1 T-audio.mp3"
transcribe_video(bucket_name, object_key)
extract_text(transcribe_video(bucket_name, object_key))