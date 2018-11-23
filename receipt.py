from google.cloud import vision, language
from PIL import Image, ImageDraw
import subprocess

# Instantiate clients for Cloud Vision and Cloud Natural Language
vision_client = vision.ImageAnnotatorClient()
language_client = language.LanguageServiceClient()

# Download the receipt image
subprocess.call('wget https://i.imgur.com/9tdZuJj.jpg'.split(' '))


# Open image with PIL to draw on it
def mask_receipt(img_path):
    source_img = Image.open(img_path)
    draw = ImageDraw.Draw(source_img)

    # Call the vision API to extract text from the image
    with open(img_path, 'rb') as f:
        image = vision.types.Image(content=f.read())

    imageresponse = vision_client.document_text_detection(image=image)
    text = ' - '.join(imageresponse.text_annotations[0].description.split('\n'))

    # Call the natural language API to extract entities for all the text we found
    document = language.types.Document(content=text, type=language.enums.Document.Type.PLAIN_TEXT)
    languageresponse = language_client.analyze_entities(document=document)

    # Collect all text that was identified as a "PERSON"
    entities = languageresponse.entities
    persons = [e.name for e in entities if e.type == 1]

    # Loop over all persons and draw black boxes over them
    for person in persons:
        for annotation in imageresponse.text_annotations[1:]:
            if annotation.description in person:
                v = annotation.bounding_poly.vertices
                box = [v[0].x, v[0].y, v[2].x, v[2].y]
                draw.rectangle(box, fill='black')

    source_img.save(img_path + '_anon', "JPEG")

mask_receipt('./9tdZuJj.jpg')