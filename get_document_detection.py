import boto3
import time
import json
import re
from json.decoder import JSONDecodeError
import os
import sys
from os import path

textract = boto3.client('textract')


def get_file_name_without_extension(fileName):
    return re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)


def start_job(s3_obj):
    response = None
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': s3_obj
        })
    return response['JobId']


def is_job_complete(jobId):
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


def detect_document(jobId):
    if(is_job_complete(jobId)):
        response = textract.get_document_text_detection(
            JobId=jobId
        )
    return response


def format_input(response):
    text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += " "+item['Text']
    return text


def save_input_format(cv_text, jobId, fileName):

    input_format_path = 'input_format/{0}.text'.format(jobId)

    if not path.exists("input_format_mapping.json"):
        with open('input_format_mapping.json', 'w+') as p:
            p.close()
    if not path.isdir("input_format"):
        os.mkdir("input_format")

    with open('input_format_mapping.json', "r+") as f:
        try:
            content = json.load(f)
            content[get_file_name_without_extension(
                fileName)] = input_format_path
            f.seek(0)
            f.truncate(0)
            f.write(json.dumps(content))
        except JSONDecodeError:
            content = {}
            content[get_file_name_without_extension(
                fileName)] = input_format_path
            f.write(json.dumps(content))

        with open(input_format_path, "w+") as outFile:
            outFile.write(json.dumps(cv_text))

        return input_format_path


if __name__ == '__main__':
    print("In poc_input")
    try:
        bucketName = sys.argv[1]
        fileName = sys.argv[2]
        s3_obj = {"Bucket": bucketName, "Name": fileName}
        jobId = start_job(s3_obj)
        response = detect_document(jobId)
        input_format = format_input(response)
        input_format_path = save_input_format(input_format, jobId, fileName)
        print('Response of Input Format Path {0}'.format(input_format_path))
    except IndexError:
        print('Please provide S3 "Bucket Name" and "File Name" while executing program.')
