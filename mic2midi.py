import mido
import numpy
import pyaudio
import signal
import sys
from mido import Message

# global definitions
CHANNELS = 1
RATE = 44100
INPUT_INDEX = 2
THRESHOLD = 0.05
NOTE = 48

# global variables
note_is_on = False
signal_is_over_threshold = False
port = None
audio = None
stream = None
    
def callback(in_data, frame_count, time_info, status_flags):
    audio_data = numpy.fromstring(in_data, dtype=numpy.float32)
    amplitude = numpy.abs(numpy.mean(audio_data))
    
    print amplitude > THRESHOLD
    if amplitude > THRESHOLD:
        if not signal_is_over_threshold:
            toggle_note_on_off()
            signal_is_over_threshold = True
    else:
        if signal_is_over_threshold:
            toggle_note_on_off()
            signal_is_over_threshold = False
    
    return (None, pyaudio.paContinue)

def toggle_note_on_off():
    if port.closed:
        print_port()
        note_is_on = False
        return
        
    note_is_on = not note_is_on
    if (note_is_on):
        port.send(Message('note_on', note=NOTE))
    else:
        port.send(Message('note_off', note=NOTE))

def open_port():
    if port.closed:
        port = mido.open_output('DSI Tetra:DSI Tetra MIDI 1 20:0')
        print_port()

def print_port():
    if port.closed:
        print "MIDI port closed"
    else:
        print "MIDI port open, connected to: ", port.name

def exit_gracefully():
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sys.exit(0)

if __name__ == "__main__":
    print "mic2midi running: ctrl+c to exit"
    signal.signal(signal.SIGINT, exit_gracefully)

    audio = pyaudio.PyAudio()
    open_port()

    stream = audio.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                input_device_index=INPUT_INDEX,
                output=False,
                input=True,
                stream_callback=callback)

    stream.start_stream()
    signal.pause()
