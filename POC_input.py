import boto3
import time
import json

textract = boto3.client('textract')

s3_obj = {"Bucket": "poc-cloudformation-bucket", "Name": "cv_test.pdf"}


def startJob(s3_obj):
    response = None
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': s3_obj
        })
    return response['JobId']


def isJobComplete(jobId):
    time.sleep(5)

    response = textract.get_document_text_detection(
        JobId=jobId
    )
    status = response['JobStatus']
    print("Job status: {}".format(status))

    while status == "IN_PROGRESS":
        time.sleep(5)
        response = textract.get_document_text_detection(
            JobId=jobId
        )
        status = response['JobStatus']
        print("Job status: {}".format(status))

    return status


def format_input(response):
    input_format = []
    id = 1
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            obj = {}
            obj['eId']=id
            obj['geometry']=item['Geometry']['BoundingBox']
            obj['text']=item['Text']
            obj['Confidence']=item['Confidence']
            input_format.append(obj)
            id+=1
    return input_format

def save_input_format(input_format,jobId):
    with open('input_format/{0}.json'.format(jobId),"w") as outFile:
        outFile.write(json.dumps(input_format))

jobId = startJob(s3_obj)
if(isJobComplete(jobId)):
    response = textract.get_document_text_detection(
        JobId=jobId
    )


input_format = format_input(response)
save_input_format(input_format,jobId)

print('--------------------------------')
print(input_format)