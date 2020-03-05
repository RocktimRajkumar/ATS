import boto3
import time
import json
import re
from json.decoder import JSONDecodeError
import os
from os import path

textract = boto3.client('textract')

fileName = "invoice.pdf"
bucketName = "poc-cloudformation-bucket"

s3_obj = {"Bucket": bucketName, "Name": fileName}


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
        if item['BlockType'] == 'LINE' and item['Page'] == 1:
            obj = {}
            obj['eId'] = id
            obj['geometry'] = item['Geometry']['BoundingBox']
            obj['text'] = item['Text']
            obj['Confidence'] = item['Confidence']
            input_format.append(obj)
            id += 1
    return input_format


def save_input_format(input_format, jobId):

    if not path.exists("input_format_mapping.json"):
        with open('input_format_mapping.json', 'w+') as p:
            p.close()
    if not path.isdir("input_format"):
        os.mkdir("input_format")

    with open('input_format_mapping.json', "r+") as f:
        try:
            content = json.load(f)
            content[re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)] = 'input_format/{0}.json'.format(jobId)
            f.seek(0)
            f.truncate(0)
            f.write(json.dumps(content))
        except JSONDecodeError:
            content = {}
            content[re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)] = 'input_format/{0}.json'.format(jobId)
            f.write(json.dumps(content))

        with open('input_format/{0}.json'.format(jobId), "w+") as outFile:
            outFile.write(json.dumps(input_format))


jobId = startJob(s3_obj)
if(isJobComplete(jobId)):
    response = textract.get_document_text_detection(
        JobId=jobId
    )


input_format = format_input(response)
save_input_format(input_format, jobId)

print('--------------------------------')
print(input_format)
