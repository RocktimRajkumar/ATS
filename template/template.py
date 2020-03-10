if __name__ != '__main__':
    from template.Rect import Rect
    from template.init import *
else:
    from Rect import Rect
    from init import *

s3 = boto3.resource('s3')


# fileName = "invoice.pdf"
# bucketName = "poc-cloudformation-bucket"

# function load predefined template co-ordinate from template.json file


def load_template(templateName):
    with open('./template/{0}.json'.format(get_file_name_without_extension(templateName)), 'r') as temp:
        template = json.load(temp)

    # Assigning image resolution to static variable of class Rect
    Rect.img_dim = template['resolution']
    return template

# function load textract block object.These objects represent lines of text or textual words that are detected on a
# document page from a json file which are formatted on the basis our requirement. And the path of this file is defined
# as a key value pair in "input_format_mapping.json"


def load_input_format(fileName):
    input_format = None
    with open('./input_format_mapping.json', 'r') as f:
        content = json.load(f)
        fileLoc = content[get_file_name_without_extension(fileName)]
        with open(fileLoc) as f:
            input_format = json.loads(f.read())
        return input_format

# This function convert the document(pdf) that is store in s3 bucket into image


def convert_pdf_to_image(bucketName, fileName):
    obj = s3.Object(bucketName, fileName)
    parse = obj.get()['Body'].read()
    images = convert_from_bytes(parse)
    return images

# Function convert the bounding box co-ordinate from the ration of overall document page into pixels of (x0,y0),(x1,y1)


def create_element_shape(input_format, images):
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


# function draw rectangle over the image using the bounding box coordinate
def draw_bounding_box(image, shapes, color):
    boxed_image = ImageDraw.Draw(image)

    for shape in shapes:
        boxed_image.rectangle(shape, outline=color)

# function group element on the basis of the template defined and save the result as json file inside template/group_element/


def grouping_element(input_formats, templates, fileName):
    group_elements = []
    for template in templates:
        group_elem = None
        group_elem = template
        elements = []
        for input_format in input_formats:
            # Converting bounding box into x0,y0,x1,y1 co-ordinate
            group = Rect(template, create='No')
            elem = Rect(input_format)

            if(group.check_element_inside_group(elem)):
                elements.append(input_format)

        group_elem["elements"] = elements
        group_elements.append(group_elem)

    if not path.isdir("template/group_element"):
        os.mkdir("template/group_element")

    with open('./template/group_element/{0}.json'.format(get_file_name_without_extension(fileName)), 'w+') as f:
        f.write(json.dumps(group_elements))
    return 'template/group_element/{0}.json'.format(get_file_name_without_extension(fileName))


if __name__ == '__main__':
    print('In template.py')
    try:
        bucketName = sys.argv[1]
        fileName = sys.argv[2]
        templateName = sys.argv[3]

        s3_obj = {"Bucket": bucketName, "Name": fileName}
        templates = load_template(templateName)
        input_format = load_input_format(fileName)
        group_elem_path = grouping_element(
            input_format, templates['group'], fileName)

        images = convert_pdf_to_image(bucketName, fileName)

        shapes = create_element_shape(input_format, images)

        draw_bounding_box(images[0], shapes, 'red')
        draw_bounding_box(images[0], list(map(
            lambda a: [(a['x0'], a['y0']), (a['x1'], a['y1'])], templates['group'])), 'green')

        images[0].show()

        print('Response of Group Element Path {0}'.format(group_elem_path))
    except IndexError:
        print('Please provide S3 "Bucket Name" and "File Name" while executing the program.')
