# Joyous-Faces

Joyous-Faces is a simple implementation of Google Cloud's AutoML Vision API to extract faces and measure the joyfulness in a photo.

## Installation

To install the necessairy packages, cd into the gdg-cloudfest folder and run:
```
pip install -r requirements.txt
```

One more step, we need to set the right environment variable for the code to use.
After the workshop, this keyfile will not work anymore.

Linux and MacOS
``` python
export GOOGLE_APPLICATION_CREDENTIALS="gdg-cloudfest-keyfile.json"
```

Windows cmd
``` bash
set GOOGLE_APPLICATION_CREDENTIALS=gdg-cloudfest-keyfile.json
```

Windows PowerShell
``` Powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="gdg-cloudfest-keyfile.json"
```

## Execution

`faces.py` defines `joyous_faces()`, which can be used to convert an image to an output outlining all faces and measuring the joyfulness factor. For instance:

    from faces import joyous_faces
    
    joyous_faces(path=os.path.join("images_input", "gdg_cloudfest.jpg"))

## Example

Input:  
<img src="https://raw.githubusercontent.com/pflammertsma/joyous-faces/master/images_input/gdg_cloudfest.jpg" width="400" />

Output:  
<img src="https://raw.githubusercontent.com/pflammertsma/joyous-faces/master/images_output/gdg_cloudfest-pop.jpg" width="400" />  
