"""
Audio player application called by subprocess
"""
import zmq
import random
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play


playerPort = '5556'
status = "BUSY"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % playerPort)


def play_audio(frequency, duration):
    tone = Sine(frequency).to_audio_segment(duration*1000)
    play(tone)


def is_tone_msg(msg):
    if ":" in msg and len(msg.split(":")) == 2:
        return True
    else:
        return False
        
if __name__ == "__main__":
    while True:
        msg = socket.recv_string()
        if msg:
            print("Messasge recived: {}".format(msg))
            msg = msg.split(":")
            socket.send_string("Playing tone")
            play_audio(int(msg[0]), int(msg[1]))
