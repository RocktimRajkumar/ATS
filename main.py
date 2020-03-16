import sys
import get_document_detection
import template.template as template
import template.detect_group_entities as detect_group_entities


try:
    bucketName = sys.argv[1]
    fileName = sys.argv[2]
    templateName = sys.argv[3]

    s3_obj = {"Bucket": bucketName, "Name": fileName}

    jobId = get_document_detection.start_job(s3_obj)
    response = get_document_detection.get_document_detection(jobId)
    input_format = get_document_detection.format_input(response)
    input_format_path = get_document_detection.save_input_format(
        input_format, jobId, fileName)

    templates = template.load_template(templateName)

    group_elem_path = template.grouping_element(
        input_format, templates['group'], fileName)

    group_element = detect_group_entities.load_group_element(fileName)
    entity_group_path = detect_group_entities.detect_entities(
        group_element, fileName)

    print('Response of Input Format Path {0}'.format(input_format_path))
    print('Response of Group Element Path {0}'.format(group_elem_path))
    print('Response of Entity Group Path {0}'.format(entity_group_path))

except IndexError:
    print('Please provide S3 "Bucket Name","File Name" and "Template Name" while executing the program.')
