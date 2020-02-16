import json
import boto3
import base64


s3 = boto3.client('s3')

BUCKET_NAME = 'poc-cloudformation-bucket'

def upload_file(event, context):
    file_content = base64.b64decode(event['content'])
    file_path = 'cv.pdf'
    try:
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content)
    except Exception as e:
        raise IOError(e)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(file_path)
    }


    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
