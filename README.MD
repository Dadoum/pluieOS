# pluieOS
pluieOS is an OS for your ra1nbox/NanoPi neo2

## pluieOS is modular
Unlike the default ra1nbox's OS, pluieOS have an application API, and a structure that permits third party apps to function. Apps implementing this API are called "Pluvieuses"

## pluieOS is dev-friendly
Pluvieuses apps are structured as following:

#### An application folder
It contains 3 essentials files:
 - app.json
 - icon.png
 - a py file

By convention, a config file should be here too, named config.json

The app.json contains these keys:
 - **name:** name of the app. It must match with the folder name. 
 - **version:** version of app.
 - **maintainer:** maintainer of the app. If the app is relying on someone else app, write the name of the person who made the Pluviales app.
 - **github:** the github of the application. If it doesn't have one, keep empty. It will permit to update the application with GitHub releases.
 - **script:** the script name. Not a path, and must have the py extension.
 - **entry_point:** the internal application name. It must match with the name of the application class in the script.

#### A script file
A script file should be equal to one application. 1 folder => 1 script => 1 app

#### An application class
An application is the core of the app (it is kinda logical, isn't it ?).
It will manage every interaction with the user through input (with buttons) and output (with screen)
These I/O are managed by a view

#### Several views
Views are the visible part of the app.
Every view should wait for an input.
It is made of:
 - One header, that is the name of the view
 - One content, what the application wants to display to the user
 - 3 actions, corresponding to the 3 buttons. F1 should be a button to edit, F2 should be a proceed button, and F3 must be a go back/exit button.

## pluieOS in the future
We plan several adds for the future:
 - Dev toolchain: actually when I write these words, when I develop, I do not test on real device but on a virtual. This is actually not ready at all for release but it works great to experiment with apps
 - Software manager: Switch between ra1nbox default OS and pluieOS easily, install updates of checkra1n, underlying Ubuntu, add apps, configure apps...

## Install pluieOS
I do not advise it. But you can by symlinking ra1nbox.py to pluieLauncher.py. If you don't know how to do it, then not do it. You can't fuck this up, but I do not guaranty any support. 

## Screenshots and code samples

App launcher:

[![https://i.imgur.com/V6aFb53.png](https://i.imgur.com/V6aFb53.png)](https://i.imgur.com/V6aFb53.png)

Sample app:

[![https://i.imgur.com/SZ3TzZi.png](https://i.imgur.com/SZ3TzZi.png)](https://i.imgur.com/SZ3TzZi.png)

Folder structure of this app:

[![https://i.imgur.com/C3wjgXI.png](https://i.imgur.com/C3wjgXI.png)](https://i.imgur.com/C3wjgXI.png)

Note: the following code samples should be taken as example, and not as how checkra1n application is made. (it has been updated)

app.json:

```json
{
	"name":"checkra1n",
	"version":"1.0.0",
	"maintainer":"dadoum",
	"github":"",
	"script":"checkra1n.py",
	"entry_point":"Checkra1nApplication"
}
```

checkra1n.py:

```python
from pluieAPI import Application, View
from PIL import Image, ImageDraw, ImageFont
import json
import subprocess
import os

class Checkra1nApplication(Application):
	def run(self, app_path):
		view = MainView()
		btn = view.run()
		if btn == 2:
			print("Launching checkra1n")
			# Get config
			app_json = os.path.join(app_path, "config.json")
			with open(app_json) as f:
				content = f.read()
			parsed_json = json.loads(content)
			options = parsed_json["options"]
			cmd_line = "-" + "".join(options)
			print ("> /usr/bin/checkra1n " + cmd_line)
			subprocess.call(["/usr/bin/checkra1n", cmd_line])
		return

class MainView(View):
	def __init__(self):
		super().__init__("checkra1n", "Options", "Start", "Exit")
		return

	def draw(self, image):
		draw = ImageDraw.Draw(image)
		draw.text((12, 12), "test", 255)
```
