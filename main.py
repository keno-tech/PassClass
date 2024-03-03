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

from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.getenv('aws_access')
aws_secret_access_key = os.getenv('secret')
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def upload_file(filename):
    """Upload a file to an S3 bucket"""
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
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
    return transcript

def run(filename):
    upload_file(filename)
    result = transcribe_video(filename)
    if result:
        t = upload_text(result, filename)
        print(t)

        return t
    
