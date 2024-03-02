import boto3
import re
import logging
import os
from botocore.exceptions import ClientError
import time
import json
import requests
from confluence import uploadTranscript

filename = "TestingVoice.mp4"
bucket_name = "videos-lecture-helper"


session = boto3.Session(
    aws_access_key_id='AKIATCKAOOBQCFQWP25S',
    aws_secret_access_key='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'
)

def upload_file(filename):
    """Upload a file to an S3 bucket"""
    s3_client = boto3.client('s3', aws_access_key_id='AKIATCKAOOBQCFQWP25S',
    aws_secret_access_key='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')
    try:
        response = s3_client.upload_file(filename, bucket_name, filename) # key will be same as the file_name
        print("uploaded successfully")
    except ClientError as e:
        logging.error(e)
        return False
    return True

def transcribe_video(filename, language_code='en-US'):
    transcribe = session.client('transcribe', region_name='ap-southeast-2')
    job_name = filename + str(time.time())
    # Replace all periods to fit into regex requirements
    job_name = re.sub(r'[^a-zA-Z0-9_-]', '_', job_name)


    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat='mp3',
        Media={
            'MediaFileUri': f's3://{bucket_name}/{filename}'
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

        return transcription_result
    else:
        print("Transcription failed.")
    return None

def extract_text(uri):
    response = requests.get(uri).json()
    print("extracted transcript: ", response["results"]["transcripts"][0]['transcript'])

def upload_text(uri, filename):
    response = requests.get(uri).json()
    transcript = response["results"]["transcripts"][0]['transcript']
    uploadTranscript(filename, transcript)

def run(filename):
    upload_file(filename)
    result = transcribe_video(filename)
    if result:
        upload_text(result, filename)

    

    

# upload_file(file_name="testingUpload3.txt")
# transcribe_video(bucket_name, object_key)
# run(filename)
run("uploads/TestingVoice.mp4")