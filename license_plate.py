from google.cloud import vision
from PIL import Image, ImageDraw
import io

def detect_document(path):
    """Detects document features in an image."""
    
    # Let's create an Image Annotator Client object on Google Cloud
    client = vision.ImageAnnotatorClient()

    # We open the file and save its contents to the variable content
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    # Also open the file in PIL so we can draw on it later
    source_img = Image.open(path)

    # Create a PIL draw object which will handle the actual drawing for us
    draw = ImageDraw.Draw(source_img)

    # We create an Image type from the image that the google cloud
    # library knows how to work with
    image = vision.types.Image(content=content)

    # Use the document text detector to search for text in the image
    # Fortunatly for us, a licence plate is text!
    response = client.document_text_detection(image=image)

    # The repsons contains all possible information the API was able to
    # gather from the image. A block represents a single piece of text it
    # was able to detect. A page is an aggregation of blocks
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # For each block of text we can show the confidence the algortihtm
            # has in that particular block
            print('\nBlock confidence: {}\n'.format(block.confidence))

            # But more importantly: we need the bounding box around the object
            # so we can paint that rectangle black and obscure the license plate
            v = block.bounding_box.vertices

            # PIL only needs the top left and bottom right corners of the 
            # rectangle to draw it properly. These are the 1st and 3rd items
            # in the vertices. PIL also needs the coordinates to be in the
            # form of [x1, y1, x2, y2]
            box = [v[0].x, v[0].y, v[2].x, v[2].y]

            # And finally we draw the black box exactly where the license
            # plate was detected
            draw.rectangle(box, fill='black')

    # Save the image with the black bars on it
    source_img.save(path + '_anon', "JPEG")


detect_document('images/car.jpg')