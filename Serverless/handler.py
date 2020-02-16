import json
import boto3
import base64



BUCKET_NAME = 'poc-cloudformation-bucket'

def upload_file(event, context):
    s3 = boto3.client('s3')
    file_content = base64.b64decode(event['content'])
    file_path = 'file.png'
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


def detectDocumentText(event, context):

    client = boto3.client('textract')
    s3_obj = {"Bucket":"poc-cloudformation-bucket", "Name":"file.png"} 
    response = client.detect_document_text(Document={"S3Object":s3_obj})
    response['DocumentMetadata']
    response['Blocks'][0]
    detect = response.copy()
    response1 = client.analyze_document(Document={"S3Object":s3_obj}, FeatureTypes=['TABLES','FORMS'])
    response1['DocumentMetadata']
    response1['Blocks'][0]

    for b in response1['Blocks']:
        if b['BlockType']=='LINE':
            print("{}\t{}".format(b['Text'],b['Confidence']))

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': '{"response": "hello"}'
    }
    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
