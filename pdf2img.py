import PIL
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('./template/invoice.pdf')
    
print(images[0])
images[0].save("./template/invoice.png", 'PNG')
