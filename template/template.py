import json
import boto3
from PIL import Image, ImageDraw
from pdf2image import convert_from_bytes
from Rect import Rect
import os
from os import path

s3 = boto3.resource('s3')


fileName = "invoice.pdf"


def load_template():
    with open('./template/template.json', 'r') as temp:
        template = json.load(temp)
    return template


def load_input_format():
    input_format = None
    with open('./input_format_mapping.json', 'r') as f:
        content = json.load(f)
        fileLoc = content[fileName]
        with open(fileLoc) as f:
            input_format = json.loads(f.read())
        return input_format


def convertPDFtoImage():
    obj = s3.Object('poc-cloudformation-bucket', fileName)
    parse = obj.get()['Body'].read()
    images = convert_from_bytes(parse)
    return images


def createShape(input_format, images):
    shapes = []
    for shape in input_format:
        normalized_bounding_box = shape['geometry']
        absolute_bounding_box_width = normalized_bounding_box['Width'] * \
            images[0].size[0]
        absolute_bounding_box_height = normalized_bounding_box['Height'] * \
            images[0].size[1]

        x0 = normalized_bounding_box['Left'] * images[0].size[0]
        y0 = normalized_bounding_box['Top'] * images[0].size[1]
        x1 = x0 + absolute_bounding_box_width
        y1 = y0 + absolute_bounding_box_height

        shape = [(x0, y0), (x1, y1)]
        shapes.append(shape)
    return shapes


def draw_bounding_box(image, shapes):
    boxed_image = ImageDraw.Draw(image)

    for shape in shapes:
        boxed_image.rectangle(shape, outline='red')
    return boxed_image


def grouping_element(input_formats, templates):
    group_elements = []
    for template in templates:
        group_elem = None
        group_elem = template
        elements = []
        for input_format in input_formats:
            group = Rect(template, create='No')
            elem = Rect(input_format)
            if(group.check_box_inside_group(elem)):
                elements.append(input_format)
        group_elem["elements"] = elements
        group_elements.append(group_elem)

    if not path.isdir("template/group_element"):
        os.mkdir("template/group_element")

    with open('./template/group_element/{0}.json'.format(fileName), 'w+') as f:
        f.write(json.dumps(group_elements))
    return group_elements


template = load_template()
images = convertPDFtoImage()
input_format = load_input_format()
shapes = createShape(input_format, images)

bounding_box_img = draw_bounding_box(images[0], shapes)

images[0].show()
# images[0].save("box.png",'PNG')

Rect.img_dim = images[0].size

group_elem = grouping_element(input_format, template['group'])
