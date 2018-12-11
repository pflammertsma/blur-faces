import io
import os
import numpy
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from google.cloud import vision

client = vision.ImageAnnotatorClient()

fontSize = 24
font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", fontSize)
fontTitle = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 50)

def joyous_faces(path):
    """
    Highlights joyous faces into an output file.

    `path` is the input filename
    """
    extract_faces('pop', path)

def extract_faces(mode, path):
    """
    Extracts faces into an output directory.

    `mode` can be one of: 'pop','blur','mask'
    `path` is the input filename
    """

    base_path = os.path.basename(path)
    anon_path = os.path.splitext(base_path)[0]
    output_path = os.path.join("images_output", "%s-%s.jpg") % (anon_path, mode)

    process_img = Image.open(path)
    source_img = process_img.convert('RGBA')
    process_img = process_img.convert('RGB')
    draw = ImageDraw.Draw(process_img)
    blur_img = source_img.filter(ImageFilter.GaussianBlur(25)).convert('RGBA')
    if mode=='pop':
        input_img = source_img
        output_img = blur_img
    elif mode=='blur':
        input_img = blur_img
        output_img = source_img

    total_faces = 0
    total_joy = 0
    expressions = []

    while True:
        # Convert image to byte array
        imgByteArr = io.BytesIO()
        process_img.save(imgByteArr, format='JPEG')

        # Process raw bytes
        image = vision.types.Image(content=imgByteArr.getvalue())
        response = client.face_detection(image=image)
        faces = response.face_annotations

        if len(faces) == 0:
            break

        for face in faces:
            total_faces += 1
            v = face.bounding_poly.vertices
            box = [v[0].x, v[0].y, v[2].x, v[2].y]

            if mode=='pop' or mode=='blur':
                temp_img = input_img.rotate(-face.tilt_angle, center=(numpy.average((v[0].x, v[2].x)), numpy.average((v[0].y, v[2].y))))
                region = temp_img.crop(box).convert('RGBA')
                regionSize = region.size
                region = region.rotate(face.tilt_angle, expand=True)
                offset = numpy.subtract(region.size, regionSize)
                output_img.paste(region, (v[0].x - offset[0]/2, v[0].y - offset[1]/2), region)

            total_joy += face.joy_likelihood - face.anger_likelihood
            expression = ('neutral', 0)
            if (face.joy_likelihood > expression[1]):
                expression = ('joy', face.joy_likelihood)
            if (face.sorrow_likelihood > expression[1]):
                expression = ('sorrow', face.sorrow_likelihood)
            if (face.anger_likelihood > expression[1]):
                expression = ('anger', face.anger_likelihood)
            if (face.surprise_likelihood > expression[1]):
                expression = ('surprise', face.surprise_likelihood)

            expression = ('%s: %d' % (expression[0], expression[1]))
            expressions.append((box, expression))

            if mode=='pop':
                print('faces popped: %d (%s)' % (total_faces, expression))
            elif mode=='blur':
                print('faces blurred: %d (%s)' % (total_faces, expression))
            else:
                print('faces masked: %d (%s)' % (total_faces, expression))

            # Mask
            draw.rectangle(box, fill='black')

    if mode=='mask':
        output_img = process_img.convert('RGBA')

    draw = ImageDraw.Draw(output_img)
    for expression in expressions:
        draw.text((expression[0][0], expression[0][1] - fontSize - 15), expression[1], color=(255,255,255), font=font)

    if (total_faces == 0): total_faces = 1
    print('joy factor: %d' % (total_joy / total_faces))

    draw.text((200, 200), ('TOTAL_JOY_FACTOR: %d' % total_joy), color=(255,255,255), font=fontTitle)

    output_img.convert('RGB').save(output_path, "JPEG")

