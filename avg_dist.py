import math
import boto3
from PIL import Image, ImageDraw
from pdf2image import convert_from_bytes
import json

s3 = boto3.resource('s3')


def load_input_format():
    input_format = None
    with open('./input_format/d3dfba257fb0ebd722ead65d188664901b51c7acc14e034030e78641864a8952.json') as f:
        input_format = json.loads(f.read())
    return input_format


class Rect:

    img_dim = 0

    def __init__(self, shape):
        super().__init__()
        normalized_bounding_box = shape['geometry']
        absolute_bounding_box_width = normalized_bounding_box['Width'] * \
            Rect.img_dim[0]
        absolute_bounding_box_height = normalized_bounding_box['Height'] * \
            Rect.img_dim[1]

        self.x0 = normalized_bounding_box['Left'] * Rect.img_dim[0]
        self.y0 = normalized_bounding_box['Top'] * Rect.img_dim[1]
        self.x1 = self.x0 + absolute_bounding_box_width
        self.y1 = self.y0 + absolute_bounding_box_height

    def dist(self, other):
        # overlaps in x or y:
        print('diff ---', self.x-other.x)
        print('width ---', self.w+other.w)

        if abs(self.x - other.x) <= (self.w + other.w):
            dx = 0
        else:
            dx = abs(self.x - other.x) - (self.w + other.w)
        #
        if abs(self.y - other.y) <= (self.h + other.h):
            dy = 0
        else:
            dy = abs(self.y - other.y) - (self.h + other.h)
        return math.sqrt(dx + dy)


def convertPDFtoImage():
    obj = s3.Object('poc-cloudformation-bucket', 'cv_test.pdf')
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




images = convertPDFtoImage()
input_format = load_input_format()
shapes = createShape(input_format, images)

bounding_box_img = draw_bounding_box(images[0], shapes)

images[0].save("./template/template.png", 'PNG')
images[0].show()

Rect.img_dim = images[0].size

# example:
# A = Rect(input_format[0])
# B = Rect(input_format[1])
# C = Rect(input_format[2])

# print(A.dist(C))
# print(A.dist(B))
# print(B.dist(C))

shapes = []

avg_dist = 0

# for i in range(0,len(input_format)):

#     for j in range(i+1,len(input_format)):
#         pass
