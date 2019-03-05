import zmq
import random
import time
import sys
import json
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
import simpleaudio as sa

class Player():
    def __init__(self, port="5557", ip="127.0.0.1"):
        self.port = port
        self.ip = ip
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect("tcp://localhost:{}".format(self.port))
        self._socket.setsockopt(zmq.SUBSCRIBE, b"")
        self._play_obj = None
        self.frequency = 60
        self.duration = 30
        self.gain = 1
        self.loops = 1

    def recieve_message(self):
        print('Listening on tcp://{}:{}'.format(self.ip, self.port))
        while True:
            msg = self._socket.recv()
            try:
                msg = json.loads(msg)
            except ValueError:
                msg = str(msg)
            if isinstance(msg, dict):
                if msg['action'] == 'play':
                    frequency = int(msg['frequency'])
                    duration = (int(msg['duration']))
                    gain = float(msg['gain'])
                    loops = int(msg['loops'])
                    self.play(frequency, duration, gain, loops)
                    # tone = Sine(int(msg["frequency"])).to_audio_segment(1000)
                    # tone = tone * int(msg['duration'])
                    # tone = tone * int(msg['loops'])
                    # tone = tone.apply_gain(int(msg['gain']))
                    # self._play_obj=sa.play_buffer(tone.raw_data,
                    #                         num_channels=tone.channels,
                    #                         bytes_per_sample=tone.sample_width,
                    #                         sample_rate=tone.frame_rate)
                    # print("Playing")
                if msg['action'] == 'stop':
                    self.stop()
                    #self.play_obj.stop()


    def stop(self):
        if self._play_obj:
            print("Stopping buffer")
            self._play_obj.stop()

    def play(self, frequency, duration, gain, loops):
        print("Playing; Frequency:{}, Duration:{}, Gain:{}, Loops:{}".format(frequency,
                                                                             duration,
                                                                             gain,
                                                                             loops))
        tone = Sine(frequency).to_audio_segment(1000)
        tone = tone * duration * loops
        tone.apply_gain(gain)
        self._play_obj=sa.play_buffer(tone.raw_data,
                                 num_channels=tone.channels,
                                 bytes_per_sample=tone.sample_width,
                                 sample_rate=tone.frame_rate)

if __name__ == "__main__":
    play_client = Player()
    play_client.recieve_message()
