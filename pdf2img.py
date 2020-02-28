import PIL
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('./template/invoiceTest.pdf',size=(1654,2339))
    
print(images[0])
images[0].save("./template/invoiceTest.png", 'PNG')
