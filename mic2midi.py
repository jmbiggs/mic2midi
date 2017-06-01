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
    
def callback(in_data, frame_count, time_info, status_flags):
    global signal_is_over_threshold

    audio_data = numpy.fromstring(in_data, dtype=numpy.float32)
    amplitude = numpy.abs(numpy.mean(audio_data))
    
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
    global ports, note_is_on

    for port in ports:
        if port.closed:
            print_ports()
            note_is_on = False
            return
        
    note_is_on = not note_is_on
    if (note_is_on):
        for port in ports:
            port.send(Message('note_on', note=NOTE))
    else:
        for port in ports:
            port.send(Message('note_off', note=NOTE))

def open_ports():
    global ports
    
    ports = []
    for port_name in mido.get_output_names():
        ports.append(mido.open_output(port_name))

    print_ports()

def print_ports():
    global ports
    
    for port in ports:
        if port.closed:
            print "MIDI port closed"
        else:
            print "MIDI port open, connected to: ", port.name

def exit_gracefully(signal, frame):
    global stream, audio
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sys.exit(0)

if __name__ == "__main__":
    global audio, stream, note_is_on, signal_is_over_threshold

    note_is_on = False
    signal_is_over_threshold = False

    print "mic2midi running: ctrl+c to exit"
    signal.signal(signal.SIGINT, exit_gracefully)

    audio = pyaudio.PyAudio()
    open_ports()

    stream = audio.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                input_device_index=INPUT_INDEX,
                output=False,
                input=True,
                stream_callback=callback)

    stream.start_stream()
    signal.pause()
