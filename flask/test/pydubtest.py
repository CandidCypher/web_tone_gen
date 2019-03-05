from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play


tone1 = Sine(100).to_audio_segment(duration=300000)



print("Playing1")
play(tone1)
print("Playing2")
play(tone2)
print("Playing3")
for i in range(0,1000):
    play(tone3)
