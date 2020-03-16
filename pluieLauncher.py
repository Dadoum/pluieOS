# -----------------------------
#      pluieOS source code
#   made with heart by dadoum
# -----------------------------
#    Partly based on rainbox
# -----------------------------

import subprocess
import sys
import time
import signal
import os
import traceback

import matplotlib as matplotlib
import numpy
import sh
import distutils.core
import urllib.request

from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
from pluieAPI import Application, View, width, height
import platform

# import bakebit_128_64_oled as display

app_path = os.path.join(os.getenv("HOME"), "Pluvieuses applications") # POA format is a compressed format that means pluieOS Application, but it corresponds to a Pluvieuses application (or correctly application pluvieuse, but we will stay simple)


# Launcher Application is an application like any application,
# Except it will never be killed until shutdown, and that it is not in the standard folder
class LauncherApp(Application):
	name = "Launcher"
	def __init__(self):
		super().__init__()

	def run(self):
		sub = os.listdir(app_path)
		import json
		# For each app
		applications = []
		jsons = []
		dirs = []
		for di in sub:
			d = os.path.join(app_path, di)
			if os.path.isdir(d):
				# We take its app.json,
				app_json = os.path.join(d, "app.json")
				with open(app_json) as f:
					content = f.read()

				# Retrieve some important values
				parsed_json = json.loads(content)
				script = os.path.join(d, parsed_json["script"])
				name = parsed_json["name"]
				entry_point = parsed_json["entry_point"]

				# And import the entry point
				import importlib.util
				spec = importlib.util.spec_from_file_location(os.path.splitext(parsed_json["script"])[0], script)
				app = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(app)
				# This is the application class
				app_class = getattr(app, entry_point)
				applications.append(app_class)
				jsons.append(parsed_json)
				dirs.append(d)


		collectionView = AppCollectionView(applications, jsons)
		while True:
			btn = collectionView.run()
			if btn == 1:
				collectionView.app_number += 1
				collectionView.reset()
			elif btn == 2:
				selected_app = applications[collectionView.app_number]
				appli = selected_app()
				appli.run(dirs[collectionView.app_number])
			elif btn == 3:
				print("shutdown")
				break
		return 0

class AppCollectionView(View):
	app_number = 0
	app_list = []
	app_jsons = []

	def __init__(self, app_list, app_jsons):
		super().__init__("Applications", "Next", "Select", "Shutdown")
		self.app_list = app_list
		self.app_jsons = app_jsons
		return

	def draw(self, image):
		draw = ImageDraw.Draw(image)
		self.app_number = self.app_number % len(self.app_list)
		app_name = str(self.app_jsons[self.app_number]["name"])
		w, h = draw.textsize(app_name, self.font)
		app_icon = os.path.join(app_path, self.app_jsons[self.app_number]["name"], "icon.png")
		img = Image.open(app_icon, 'r')
		img_w, img_h = img.size
		image.paste(img, (5, int((height - (img_h + (h / 2))) / 2)))
		draw.text(((width - w - 5), (height - h) / 2), (app_name), 255)
		return

def launch():
	try:
		launcher = LauncherApp()
		exitCode = launcher.run()
	except:
		try:
			print(traceback.print_exc())
		except:
			"nothing"
		exitCode = 1

	if exitCode != 0:
		print("Launcher crashed !")
		from pluieAPI import draw, image
		draw.rectangle((0, 0, width, height), 0)
		draw.text((0, 0), "Launcher crashed :(", 255)
		image.save("./debug.png")

launch()

