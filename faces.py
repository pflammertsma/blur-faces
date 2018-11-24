from google.cloud import vision
from PIL import Image, ImageDraw

import io
import os

def mask_faces(path):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    source_img = Image.open(path)
    draw = ImageDraw.Draw(source_img)

    for face in faces:

        v = face.bounding_poly.vertices

        box = [v[0].x, v[0].y, v[2].x, v[2].y]

        draw.rectangle(box, fill='black')

    base_path = os.path.basename(path)
    anon_path = os.path.splitext(base_path)[0]
    source_img.save(os.path.join("anon_images", "%s.jpg") % anon_path, "JPEG")

mask_faces(os.path.join("images", "car_and_person.jpg"))