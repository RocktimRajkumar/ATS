import boto3
import time
import json
import re
from json.decoder import JSONDecodeError
import os
import sys
from os import path
from PIL import Image, ImageDraw
from pdf2image import convert_from_bytes

textract = boto3.client('textract')


def get_file_name_without_extension(fileName):
    return re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)
