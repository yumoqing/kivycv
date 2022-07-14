import os
import pickle
from functools import partial
import wave
import pyaudio
import time
import tempfile

from appPublic.app_logger import AppLogger, create_logger

class Audio(AppLogger, pyaudio.PyAudio):
	def __init__(self, save_file=None):
		AppLogger.__init__(self)
		pyaudio.PyAudio.__init__(self)
		self.temp_filename = None
		self.chunk = 1024
		self.devices = [ self.get_device_info_by_index(i) \
								for i in range(self.get_device_count()) ]
		self.recording = False

	def get_input_device(self):
		return [ d for d in self.devices if d.maxInputChannels > 0 ]

	def get_output_device(self):
		return [ d for d in self.devices if d.maxOutputChannels > 0 ]

	def tmpfile(self):
		x = tempfile.mkstemp(suffix='.wav')
		os.close(x[0])
		self.temp_filename = x[1]
		return self.temp_filename

	def record_cb(self, in_data, frame_count, time_info, status):
		self.wavfile.writeframesraw(in_data)
		if self.recording:
			return (None, pyaudio.paContinue)
		return (None, pyaudio.paComplete)

	def replay_cb(self, in_data, frame_count, time_info, status):
		data = self.wavfile.readframes(frame_count)
		if not data:
			return (None, pyaudio.paComplete)

		return (data, pyaudio.paContinue)

	def get_output_index(self):
		dev_cnt = self.get_device_count()
		for i in range(dev_cnt):
			x = self.get_device_info_by_index(i)
			print(x)
		return dev_cnt - 1

	def write_audiofile(self, fn, audio_data, channels=2, rate=44100):
		wf = wave.open(fn, 'wb')
		wf.setnchannels(channels)
		wf.setsampwidth(2)
		wf.setframerate(rate)
		wf.writeframesraw(audio_data)
		wf.close()

	def start_record(self, 
						savefile=None, 
						channels=2,
						rate=44100
		):
		if savefile is None:
			savefile = self.tmpfile()
		self.save_file = savefile
		self.wavfile = wave.open(self.save_file, 'wb')
		self.wavfile.setnchannels(channels)
		self.wavfile.setsampwidth(2)
		self.wavfile.setframerate(rate)
		self.stream = self.open(format=pyaudio.paInt16,
						channels=channels,
						rate=rate,
						input=True,
						frames_per_buffer=self.chunk,
						stream_callback=self.record_cb)
		self.stream.start_stream()
		self.recording = True

	def stop_record(self):
		if self.recording:
			self.recording = False
			self.stream.stop_stream()
			self.stream.close()
			self.wavfile.close()

	def record(self, stop_cb,
						savefile=None, 
						channels=2,
						rate=44100,
		):
		self.start_record(savefile=savefile, channels=channels,rate=rate)
		while  not stop_cb():
			time.sleep(0.1)
		self.stop_record()

	def get_audio_spec(self, audiofile):
		wavfile = wave.open(audiofile, 'rb')
		sampwidth = wavfile.getsampwidth()
		format = self.get_format_from_width(sampwidth)
		framerate=wavfile.getframerate()
		channels = wavfile.getnchannels()
		return {
			"format":format,
			"sampwidth":sampwidth,
			"framerate":framerate,
			"channels":channels
		}
		
	def replay(self, play_file=None):
		idx = self.get_output_index()
		x = self.get_device_info_by_index(idx)
		y = self.get_default_input_device_info()
		if play_file is None:
			play_file = self.temp_filename
		self.wavfile = wave.open(play_file, 'rb')
		format = self.get_format_from_width(self.wavfile.getsampwidth())
		framerate=self.wavfile.getframerate()
		self.stream = self.open(format=format,
						channels=self.wavfile.getnchannels(),
						rate=framerate,
						output=True,
						output_device_index=idx,
						frames_per_buffer=self.chunk,
						stream_callback=self.replay_cb)
		self.stream.start_stream()
		while self.stream.is_active():
			time.sleep(0.05)
		self.stream.stop_stream()
		self.stream.close()
		self.wavfile.close()

if __name__ == '__main__':
	import sys
	t_begin = time.time()
	def stop_func(audio):
		t = time.time()
		if t - t_begin >= 10:
			return True
		return False

	create_logger('audio', levelname='debug')
	a = Audio()
	
	if 'replay' in sys.argv[0]:
		if len(sys.argv) < 2:
			print(f'usage:\n{sys.argv[0]} WAVFILE')
			sys.exit(1)
		a.replay(sys.argv[1])
	elif 'record' in sys.argv[0]:
		sf = None
		if len(sys.argv) >= 2:
			sf = sys.argv[1]
		f = partial(stop_func, a)
		a.record(f, savefile=sf)
