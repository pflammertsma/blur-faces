from google.cloud import vision, language
from PIL import Image, ImageDraw

import os
import io

# Instantiate clients for Cloud Vision and Cloud Natural Language
vision_client = vision.ImageAnnotatorClient()
language_client = language.LanguageServiceClient()


# Open image with PIL to draw on it
def mask_receipt(path):
    source_img = Image.open(path)
    draw = ImageDraw.Draw(source_img)

    # Call the vision API to extract text from the image
    with io.open(path, 'rb') as f:
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
    
    base_path = os.path.basename(path)
    anon_path = os.path.splitext(base_path)[0]
    source_img.save(os.path.join("anon_images", "%s.jpg") % anon_path, "JPEG")

mask_receipt(os.path.join("images", "receipt.jpg"))