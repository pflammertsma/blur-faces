
#Step 1: Clone the repo

To clone the repo, open a terminal/cmd window and cd into an appropriate folder. Then run the git clone command:

```
git clone git@bitbucket.org:ml6team/gdg-cloudfest.git
```

#Step 2: Install packages

To install the necessairy packages, cd into the gdg-cloudfest folder and run:

```
pip install --upgrade google-cloud-vision google-cloud-language Pillow
```

#Step 3: Set keyfile in environment

One more step, we need to set the right environment variable for the code to use.
After the workshop, this keyfile will not work anymore.

Linux and MacOS
``` python
export GOOGLE_APPLICATION_CREDENTIALS="gdg-cloudfest-keyfile.json"
```

Windows cmd
``` python
set GOOGLE_APPLICATION_CREDENTIALS=gdg-cloudfest-keyfile.json
```

Windows PowerShell
``` python
$env:GOOGLE_APPLICATION_CREDENTIALS="gdg-cloudfest-keyfile.json"
```

Have fun!