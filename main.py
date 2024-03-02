import boto3
import logging
import os
from botocore.exceptions import ClientError
import time
from urllib.request import urlopen
import json

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
    except ClientError as e:
        logging.error(e)
        return False
    return True

def transcribe_video(filename, language_code='en-US'):
    transcribe = session.client('transcribe', region_name='ap-southeast-2')
    job_name = filename + str(time.time())

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

def extract_text(url):
    response = urlopen(url)
    data = json.loads(response.read())
    print(data["results"]["transcripts"][0]['transcript'])

def run(filename):
    upload_file(filename)
    result = transcribe_video(filename)
    if result:
        extract_text(result)

# upload_file(file_name="testingUpload3.txt")
# transcribe_video(bucket_name, object_key)
# run(filename)
extract_text("https://s3.ap-southeast-2.amazonaws.com/aws-transcribe-ap-southeast-2-prod/211125432416/TestingVoice.mp41709351498.162453/7930505b-0838-41e9-847e-e821ccb6ca6c/asrOutput.json?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEMaDmFwLXNvdXRoZWFzdC0yIkYwRAIgOsEb3iIiSVFfWY0GXxqz1dEhVlOPNCGSBHhIbX24F5wCIArGy87XJOxULlnFv9HoWhjBAkTe%2FVec3TufOwEqAMI0KsgFCDwQBBoMNzQwNDg3NzYxMjI4Igz%2Bi%2F8O4So8IAvot%2BUqpQVqDKFBNVSXtsBJ7%2FCe6qopcwrxinVEDfVTJkZLLCyLJxfSMHC4TN1cr3rfyf1WmOTLFtBq%2Bwaik%2FZwynt8wSXspeTVwS7vJFVs%2FrOxdT%2BTxyieZy8gPlCOJlucb6UvhNbxv5NKfSZKpgUMz%2FgEVpG1q%2Fk6JhMKG3kzykOlPoUNKdTtvYfEBxKh5PsyNXICkLlpg%2BehCj3u%2FJsppc9KdVIgKyJBWx0KgNcm0%2FdhiZ98HkV4%2BMpZ6xVhE1drAI5EpqFJVTnYw44YsjxlvllWgRv0jZh9KT%2BBX2q3fkPt1vITSmRuoXAMxQPE4bEpJEDjsxd7YExsbm45CRVP1dChAFDJzGms6dEClCKBV3%2FFnbR0kKdvd12GBGIVKgrl5Pfjg5YR3p3CAhYjRJIW4X8HabZ9Dvyfodr2FTAsfzUqAseOIlKnixwNN2GB3qLuqryv8F0HEHJfNwCsBj854q6VfkT84rSyBzMo1E3H2KF7IWQ%2BwjQvS%2BuT1yeZ5Psr4JtETMI1wCQAasEE1aVTI1MzvcbH8z%2Fs8DDq3TBnX2WPTCVfZUJcGFh1IQmxRc1X7HvbutIRtASFEV4Qq5GUC79GKC6Z%2FHM0DUiH%2FTJj9cxXtO9JIWmyz5ppaLsz7NYPa%2B86WCX4sjDmTjScPjL75lnzeWoOFXWtFWyalRVHQ%2BKLJhFYt5ObEYwXlo2TlcWQ7bd1dWvSsn3Mqe1mBjV8MTAjIZJkkpO6vV4zWy517TUzq23%2Be71jWy56%2FDJa7DXvZGa4lug7rfVtGTEjpp85EcibvkpYv7kBQ31viayqgSg3G8Ei1kwwXcq8H2pwk96CeszX4Ki%2FohHEF1NtwUsqiGU91DMXp38bqTEfw31KwuGASg1uT4j9XD6J1fffisAE18097F%2FvkGDejjCApIqvBjqyAbwPISIIEwDOhl9oo5u1TSHra2Ntk7TTRMXEFhGdU9%2B1CoChpWh4gWcEjB7yvfKUxwesdTrLRjwKTbuzKcD6Xm6f0jh1IA3w6oijYQVxtV8Uhuqzuse9d%2BHxVrSzv7Rktq2lO4s3E5aPaweM%2FQdPaD%2B73Cl9FSZYMCqEgIMqU01OzrLJFLFmwrzcfdq869cfCT3nUxEMShndwuzGvpHxWQwpjuZ3ayt9KGAcHhVPzaSSc1E%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240302T035145Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=ASIA2Y2ECRVGLKA7OVWI%2F20240302%2Fap-southeast-2%2Fs3%2Faws4_request&X-Amz-Signature=c7e030931fde90786c2fdc5fc06ffc621b8dd21cfe5ea6c0dcc04673129ed4fb")
