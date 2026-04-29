import mido

from tkinter import *
from tkinter import ttk

import math
import random
import time
import sys

class Config:
	num_speakers = 8
	is_2if = True
	num_sounds = 4
	base_note = 36
	num_each_test = 2
	base_controller = 12

class Test:
	def __init__(self, sound_idx, speaker_idx):
		self.sound_idx = sound_idx
		self.speaker_idx = speaker_idx
		self.sound_time = None

root = Tk()

root.title("N-speaker localisation tester")
root.geometry("600x600")
frame = ttk.Frame(root).grid(column=0, row=0, sticky=(N, W, E, S))


midi_out = mido.open_output(mido.get_output_names()[1])

class Tester:
	def __init__(self):
		self.test_num = 0
		self.current_test = None

		self.tests = []
		for speaker in range(Config.num_speakers):
			for sound in range(Config.num_sounds):
				self.tests.append([speaker, sound])
		
		self.tests = self.tests * Config.num_each_test

		random.shuffle(self.tests)
		print(self.tests)

	def start_test(self):
		if self.current_test:
			return
		if self.test_num == len(self.tests):
			print("test complete!", file = sys.stderr)
			return
		test = self.tests[self.test_num]
		speaker = test[0]
		sound = test[1]
		
		self.current_test = Test(
			sound,
			speaker
		)
		root.after(1000, self.play_test)

	def play_test(self):
		note = Config.base_note + self.current_test.sound_idx
		msg = mido.Message("note_on", note = note, channel = self.current_test.speaker_idx)
		midi_out.send(msg)
		self.current_test.sound_time = time.time()

	def end_test(self, guess):
		if self.current_test == None:
			return
		if self.current_test.sound_time == None: # check if test has been played yet
			return
		data = [self.current_test.speaker_idx, self.current_test.sound_idx, guess, self.current_test.sound_time, time.time()]
		print(",".join([str(x) for x in data]))
		self.current_test = None
		self.test_num += 1

tester = Tester()

def on_press(n):
	tester.end_test(n)

def make_button(parent, idx):
	angle_per = 360 / Config.num_speakers
	base_angle = 0
	if Config.is_2if:
		base_angle = angle_per / 2
	angle = base_angle + (angle_per * idx)
	angle = math.radians(angle)
	x = (math.sin(angle) * 0.4) + 0.5
	y = (math.cos(angle) * -0.4) + 0.5
	ttk.Button(parent, text=idx + 1, command=lambda : on_press(idx)).place(anchor="center", relx=x, rely=y, height=100, width=100)

for x in range(Config.num_speakers):
	make_button(frame, x)

ttk.Button(frame, text="start", command=tester.start_test).place(anchor="center", relx=0.5, rely=0.5, height=150, width=150)

root.mainloop()

print("exiting")
msg = mido.Message("control_change", control = 123) # all notes off
midi_out.send(msg)
