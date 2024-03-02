import boto3

def delete_transcription_job(job_name):
    # Initialize the Transcribe client with the desired region
    transcribe = boto3.client('transcribe', region_name='ap-south-1')

    # Delete the transcription job
    response = transcribe.delete_transcription_job(
        TranscriptionJobName=job_name
    )

    # Print response
    print(response)

# Example usage
job_name = "transribe-job"
delete_transcription_job(job_name)
