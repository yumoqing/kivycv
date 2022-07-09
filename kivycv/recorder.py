import pyaudio
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivyblocks.baseWidget import HBox, VBox
import os
import sys
import time
try:
	from .audio import Audio
except:
	from audio import Audio

class Recorder(VBox):
	rate = NumericProperty(44100)
	channel = NumericProperty(2)
	def __init__(self, **kw):
		super().__init__(**kw)
		self.audio = Audio()
		self.register_event_type('on_recorded')

	def on_recorded(self, record_file):
		print('on_recorded:', record_file)

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.audio.start_record(channels=self.channel,
									rate=self.rate)
			return False
		return super().on_touch_down(touch)

	def on_touch_up(self, touch):
		if self.audio.recording:
			self.audio.stop_record()
			self.dispatch('on_recorded', self.audio.save_file)

		return super().on_touch_up(touch)

if __name__ == '__main__':
	from kivy.app import App
	class TestApp(App):
		def build(self):
			x = Recorder()
			self.recorder = x
			x.bind(on_recorded=self.play_audio)
			return x

		def play_audio(self, o, f):
			print('play file', f)
			self.recorder.audio.replay(f)
			print('play finished')
			# os.remove(f)

	TestApp().run()
