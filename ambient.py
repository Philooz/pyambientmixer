"""ambient.py - plays an ambient mix with pygame. Mash CTRL+C to quit.
 
Usage:
  ambient.py <file>
 
Options:
  <file>             XML file of the ambient mix to play. Make sure you have the correct "sounds/" folder in your current working directory.
  -h --help          Show this help message.

"""
__author__      = "Philooz"
__copyright__   = "2017 GPL"

import random, sys
import pygame, untangle

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

clock = pygame.time.Clock()

CLOCK_TICKER = 10

unit_duration_map = {
	'1m': 60*CLOCK_TICKER,
	'10m': 600*CLOCK_TICKER,
	'1h': 3600*CLOCK_TICKER
}

def chop_interval(num, prec, max, len):
	values = []
	num += 1
	for i in range(num):
		values.append(random.randint(0, prec))
	norm = sum(values)
	anc = 0
	max_ar = max - 1.5*len*num
	for i in range(num):
		old = values[i]
		values[i] += anc
		anc += old
		values[i] /= norm
		values[i] *= max_ar+i*1.5*len
		values[i] = int(values[i])
	return values

class Channel():
	def __init__(self, channel_id, sound_id, name = "", volume = 100, random = False, random_counter = 1, random_unit = "1h", mute = False, balance = 0):
		try:
			self.sound_object = pygame.mixer.Sound("sounds/{}.ogg".format(sound_id))
		except:
			print('Error while loading sound "sounds/{}.ogg". Did you convert it to ogg?'.format(sound_id))
			sys.exit()
		self.channel_object = pygame.mixer.Channel(channel_id)
		self.name = name
		#Normalize volume
		self.volume = volume
		self.sound_object.set_volume(int(volume)/100.0)
		#Adjust balance
		self.balance = balance
		self.left_volume = 1.0 if (balance <= 0) else (1.0-float(balance)/100)
		self.right_volume = 1.0 if (balance >= 0) else (1.0+float(balance)/100)
		self.channel_object.set_volume(self.left_volume, self.right_volume)
		#Set random
		self.channel_id = channel_id
		self.sound_id = sound_id
		self.random = random
		self.random_counter = random_counter
		self.random_unit = random_unit
		self.play_at = []
		self.current_tick = 0
		self.mute = mute
	
	def __repr__(self):
		if(self.random):
			return "Channel {channel_id} : {name} (random {ran} per {unit}), {sound_id}.ogg (volume {vol}, balance {bal})".format(
			channel_id=self.channel_id,
			name=self.name,
			sound_id=self.sound_id,
			vol=self.volume,
			bal=self.balance,
			ran=self.random_counter,
			unit=self.random_unit)
		else:
			return "Channel {channel_id} : {name} (looping), {sound_id}.ogg (volume {vol}, balance {bal})".format(
			channel_id=self.channel_id,
			name=self.name,
			sound_id=self.sound_id,
			vol=self.volume,
			bal=self.balance)

	def compute_next_ticks(self):
		val = unit_duration_map[self.random_unit]
		sound_len = self.sound_object.get_length()*1.5
		self.play_at = chop_interval(self.random_counter, 100, val, sound_len)

	def play(self, force = False):
		if(not self.random and not self.mute):
			self.channel_object.play(self.sound_object, loops = -1)
		if(force):
			self.channel_object.play(self.sound_object)

	def tick(self):
		if(self.random and not self.mute):
			if(len(self.play_at) > 0):
				self.current_tick += 1
				ref = self.play_at[0]
				if(self.current_tick > ref):
					#print("Playing : {}".format(self.play_at))
					self.play_at.pop(0)
					if(len(self.play_at) >= 1):
						self.play(True)
			else:
				self.current_tick = 0
				self.compute_next_ticks()
				#print("Recomputed : {}".format(self.play_at))

def load_file(xml_file):
	obj = untangle.parse(xml_file)
	ls = []
	for chan_num in range(1,9):
		channel = getattr(obj.audio_template, "channel{}".format(chan_num))
		dic = {}
		dic["sound_id"] = channel.id_audio.cdata
		dic["random"] = (channel.random.cdata == "true")
		dic["mute"] = (channel.mute.cdata == "true")
		dic["name"] = channel.name_audio.cdata
		dic["volume"] = channel.volume.cdata
		dic["balance"] = int(channel.balance.cdata)
		dic["random_counter"] = int(channel.random_counter.cdata)
		dic["random_unit"] = channel.random_unit.cdata
		ls.append(dic)
	return ls

def bootstrap_chanlist(chans_to_load):
	channels = []
	for(c_id, c_val) in enumerate(chans_to_load):
		if c_val["sound_id"] not in ('','0'):
			channels.append(Channel(c_id, **c_val))
	for channel in channels:
		print('Loaded {}.'.format(channel))
	for channel in channels:
		channel.play()
	print('Press CTRL+C to exit.')
	while True:
		clock.tick(CLOCK_TICKER)
		for channel in channels:
			channel.tick()

from docopt import docopt
if __name__ == "__main__":
	arguments = docopt(__doc__, version = '0.1ß')
	bootstrap_chanlist(load_file(arguments.get('<file>')))