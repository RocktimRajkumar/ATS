if __name__ != '__main__':
    from template.init import *
else:
    from init import *

comprehend = boto3.client('comprehend')


def load_group_element(fileName):
    with open('./template/group_element/{0}.json'.format(re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)), 'r') as elem:
        group_element = json.load(elem)
    return group_element


def detect_entities(group_element, fileName):
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

    with open('./template/entity_group_element/{0}.json'.format(re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)), 'w+') as f:
        f.write(json.dumps(entity_group))

    return './template/entity_group_element/{0}.json'.format(re.search(r"^(.+)(\.[^.]*)$", fileName).group(1))


if __name__ == '__main__':
    print('In detect_group_entities.py')
    try:
        fileName = sys.argv[1]
        group_element = load_group_element(fileName)
        entity_group_path = detect_entities(group_element, fileName)
        print('Response of Entity Group Path {0}'.format(entity_group_path))
    except IndexError:
        print('Please provide S3 "File Name" while executing the program.')
