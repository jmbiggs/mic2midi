import pyaudio
import numpy
from matplotlib import pyplot
import scipy.signal as signal
import time

import mido
from mido import Message

CHANNELS = 1
RATE = 44100
INPUT_INDEX = 2

#class MidiConverter:
#    current_note = 48

#    def __init__(self):

#    def convert_input_to_midi(self):
    
def callback(in_data, frame_count, time_info, status_flags):
    global b,a,fulldata,dry_data,frames
    audio_data = numpy.fromstring(in_data, dtype=numpy.float32)
    dry_data = numpy.append(dry_data,audio_data)

    fulldata = numpy.append(fulldata,audio_data)

    return (None, pyaudio.paContinue)

def close_audio():
    global stream,audio
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    print "mic2midi running: ctrl+c to exit"

#    converter = MidiConverter()

    audio = pyaudio.PyAudio()
    fulldata = numpy.array([])
    dry_data = numpy.array([])

    stream = audio.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                input_device_index=INPUT_INDEX,
                output=False,
                input=True,
                stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(10)
        stream.stop_stream()
    stream.close()

    numpydata = numpy.hstack(fulldata)
    pyplot.plot(numpydata)
    pyplot.show()

    audio.terminate()


