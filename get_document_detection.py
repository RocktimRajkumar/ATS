
from template.init import *


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


def get_document_detection(jobId):
    if(is_job_complete(jobId)):
        response = textract.get_document_text_detection(
            JobId=jobId
        )
    return response


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


def save_input_format(input_format, jobId, fileName):

    input_format_path = 'input_format/{0}.json'.format(jobId)

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
            outFile.write(json.dumps(input_format))

        return input_format_path


if __name__ == '__main__':
    print("In poc_input")
    try:
        bucketName = sys.argv[1]
        fileName = sys.argv[2]
        s3_obj = {"Bucket": bucketName, "Name": fileName}
        jobId = start_job(s3_obj)
        response = get_document_detection(jobId)
        input_format = format_input(response)
        input_format_path = save_input_format(input_format, jobId, fileName)
        print('Response of Input Format Path {0}'.format(input_format_path))
    except IndexError:
        print('Please provide S3 "Bucket Name" and "File Name" while executing program.')
