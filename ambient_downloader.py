"""ambient_downloader.py - download an ambient XML file from ambient-mixer.com
 
Usage:
  ambient_downloader.py <url>
 
Options:
  <url>				 URL of the ambient mix.
  -h --help          Show this help message.
 
"""
__author__      = "Philooz"
__copyright__   = "2017 GPL"

import re, os

import requests
import untangle

template_url = "http://xml.ambient-mixer.com/audio-template?player=html5&id_template="
re_js_reg = re.compile(r"AmbientMixer.setup\('#mixer-gui-box', ([0-9]+)\);")

def makedirs():
	if not os.path.exists("sounds"):
		os.makedirs("sounds")
	if not os.path.exists("presets"):
		os.makedirs("presets")

def download_file(url, save = False, filename = None):
	if(len(url.strip()) == 0):
		return
	response = requests.get(url)
	if(save):
		if filename is None:
			filename = url.split('/')[-1]
		with open(filename, "wb") as file:
			file.write(response.content)
		print("Saved {} as {}.".format(url, filename))
	else:
		return response.text

def get_correct_file(url, filename = None):
	if(filename is None):
		filename = url.split("/")[-1]
	if(not url.startswith(template_url)):
			page = download_file(url)
			val = re_js_reg.findall(str(page))[0]
			url = template_url + val
	fname = os.path.join("presets", "{}.xml".format(filename))
	download_file(url, True, fname)
	return fname

def download_sounds(xml_file):
	obj = untangle.parse(xml_file)
	for chan_num in range(1,9):
		channel = getattr(obj.audio_template, "channel{}".format(chan_num))
		new_filename = channel.id_audio.cdata
		url = channel.url_audio.cdata
		ext = url.split('.')[-1]
		filename = os.path.join("sounds", new_filename + "." + ext)
		filename_ogg = os.path.join("sounds", new_filename + ".ogg")
		if not(os.path.exists(filename) or os.path.exists(filename_ogg)):
			download_file(url, True, filename)


from docopt import docopt
if __name__ == "__main__":
	arguments = docopt(__doc__, version = '0.1ß')
	makedirs()
	download_sounds(get_correct_file(arguments.get('<url>')))
