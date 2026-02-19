import mido

from tkinter import *
from tkinter import ttk

import math
import random
import time

class Config:
	num_speakers = 2
	is_2if = True
	num_sounds = 4
	base_note = 57
	num_tests = 16
	base_controller = 16

class Test:
	def __init__(self, sound_idx, speaker_idx):
		self.sound_idx = sound_idx
		self.speaker_idx = speaker_idx
		self.sound_time = None

root = Tk()
midi_out = mido.open_output()

class Tester:
	def __init__(self):
		self.test_num = 0
		self.current_test = None

	def start_test(self):
		if self.current_test:
			return
		speaker = random.randrange(Config.num_speakers)

		for x in range(Config.num_speakers):
			midi_out.send(mido.Message("control_change", control = 16 + x, value = 0))

		midi_out.send(mido.Message("control_change", control = 16 + speaker, value = 32))

		self.current_test = Test(
			random.randrange(Config.num_sounds),
			speaker
		)
		root.after(1000, self.play_test)

	def play_test(self):
		note = Config.base_note + self.current_test.sound_idx
		msg = mido.Message("note_on", note = note)
		midi_out.send(msg)
		self.current_test.sound_time = time.time()

	def end_test(self, guess):
		if self.current_test.sound_time == None: # check if test has been played yet
			return
		msg = mido.Message("control_change", control = 123) # all notes off
		midi_out.send(msg)
		data = [self.current_test.speaker_idx, self.current_test.sound_idx, self.current_test.sound_time, time.time()]
		print(",".join([str(x) for x in data]))
		self.current_test = None
		#self.start_test()

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
	ttk.Button(parent, text=idx, command=lambda : on_press(idx)).place(anchor="center", relx=x, rely=y, height=150, width=150)

root.title("N-speaker localisation tester")
root.geometry("1000x1000")
frame = ttk.Frame(root).grid(column=0, row=0, sticky=(N, W, E, S))

for x in range(Config.num_speakers):
	make_button(frame, x)

ttk.Button(frame, text="start", command=tester.start_test).place(anchor="center", relx=0.5, rely=0.5, height=150, width=150)

root.mainloop()

print("exiting")
msg = mido.Message("control_change", control = 123) # all notes off
midi_out.send(msg)
