# mic2midi

Python script intended for Linux / Raspberry Pi use.  Converts microphone input into a MIDI note.  A threshold level is set - when audio input is above the threshold, the note will turn on, and when input drops below it, the note turns off.

## Getting Started

### Prerequisites

[PyAudio](https://people.csail.mit.edu/hubert/pyaudio)

[NumPy](http://www.numpy.org/)

[Mido](https://github.com/mido/mido)

[rtmidi](https://github.com/thestk/rtmidi)

### Installing

1. [Install PyAudio using the method of your choice](https://people.csail.mit.edu/hubert/pyaudio)
Example:
```
pip install pyaudio
```

2. [Install NumPy using the method of your choice](https://www.scipy.org/install.html)
Example:
```
sudo apt-get install python-numpy
```

3. Install Mido
```
pip install mido
```

4. Install rtmidi
```
pip install python-rtmidi
```

### Usage

You can edit the global definitions in the script to get the functionality you want.

INPUT_INDEX is the port number for your audio input.  You can figure it out by using the input.py script.

THRESHOLD is the amount of input at which you want the MIDI note to trigger.

NOTE is the number of the MIDI note you want to trigger.


## Author

jmbiggs, [jmbiggsdev@gmail.com](mailto:jmbiggsdev@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
