import boto3
import json
import os
from os import path

fileName = "myInvoice.pdf.json"


def load_template():
    with open('./template/group_element/'+fileName, 'r') as elem:
        group_element = json.load(elem)
    return group_element


def detect_entities(group_element):
    entity_group = []
    for group in group_element:
        entities = {}
        for element in group['elements']:
            text = element['text']
            response = comprehend.detect_entities(LanguageCode='en', Text=text)
            for entity in response['Entities']:
                if entity['Type'] not in entities:
                    entities[entity['Type']] = entity['Text']
                else:
                    if isinstance(entities[entity['Type']], list):
                        entities[entity['Type']].append(entity['Text'])
                    else:
                        arr = []
                        arr.append(entities[entity['Type']])
                        arr.append(entity['Text'])
                        entities[entity['Type']] = arr
        group['Entities'] = entities
        entity_group.append(group)

    if not path.isdir("template/entity_group_element"):
        os.mkdir("template/entity_group_element")

    with open('./template/entity_group_element/{0}.json'.format(fileName), 'w+') as f:
        f.write(json.dumps(entity_group))

    return entity_group


group_element = load_template()

comprehend = boto3.client('comprehend')

entity_group = detect_entities(group_element)
