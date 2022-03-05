from music21 import *
from midi2audio import FluidSynth
import os
import random
import json
import itertools


alt = json.load(open("datos.json"))["alteraciones"]
modes = json.load(open("datos.json"))["modes"]


def nice_name(l):
    s = ""
    for i in l:
        if str(i.spanish) in alt:
            s += ", " + alt[str(i.spanish)]
        else:
            s += ", " + str(i.spanish)

    return s[2:].title()


class Sequence:

    def __init__(self, k, m, n, fund=bool):
        self.key = k #Key
        self.m = eval(modes[m]) #Mode
        self.key_sign = self.get_key() # Armadura de clave
        self.n = n #Number of notes in sequence
        self.tkey = meter.TimeSignature(str(n) + "/" + str(4))
        self.fund = eval(fund)
        self.scale_names = [str(i) for i in self.m(self.key).getPitches(self.key + "4", self.key + "5")]
        self.scale_pitches = [i for i in self.m(self.key).getPitches(self.key + "4", self.key + "5")]
        self.seq_names = self.fundamental()
        self.seq_pitches = [pitch.Pitch(i) for i in self.seq_names]

    def get_key(self):
        modes = {"<class 'music21.scale.MinorScale'>": [0, "minor"],
                 "<class 'music21.scale.HarmonicMinorScale'>": [0, "minor"],
                 "<class 'music21.scale.MajorScale'>": [1, "major"]}
        roots = {"Cb": "c-", "Db": "d-", "Eb": "e-", "Fb": "f-", "Gb": "g-", "Ab": "a-", "Bb": "b-", "C": "c", "D": "d",
                 "E": "e", "F": "f", "G": "g", "A": "a", "B": "b", "C#": "c#", "D#": "d#", "E#": "e#", "F#": "f#",
                 "G#": "g#", "A#": "a#", "B#": "b#"}
        fund = roots[self.key]
        mode = modes[str(self.m)][1]
        if modes[str(self.m)][1] == "major":
            fund = fund.upper()
        k = key.Key(fund, mode)
        return k

    def fundamental(self):
        if self.fund:
            f = list(itertools.chain([self.scale_names[0]], random.sample(self.scale_names, self.n - 1)))
        else:
            f = self.seq_names = random.sample(self.scale_names, self.n)
        return f

    def get_scale_audio(self):
        st = stream.Stream()
        for i in self.scale_names:
            st.append(note.Note(i))
        st.write("midi", "escala.mid")
        fs = FluidSynth()
        s = fs.midi_to_audio("escala.mid", "escala.wav")
        os.remove("escala.mid")
        return s

    def get_seq_audio_bank(self, path, name, ext): # Path, Name, Ext midi o audio
        print(path + "--" + name)
        st = stream.Stream()
        for i in self.seq_names:
            st.append(note.Note(i, quarterLength=2))
        st.write("midi", path + "/" + name + ".mid")
        if ext == "audio":
            fs = FluidSynth()
            fs.midi_to_audio(path + "/" + name + ".mid", path + "/" + name + ".flac")
            os.remove(path + "/" + name + ".mid")

    def get_seq_audio(self):
        st = stream.Stream()
        for i in self.seq_names:
            st.append(note.Note(i, quarterLength=2))
        st.write("midi", "seq.mid")
        fs = FluidSynth()
        s = fs.midi_to_audio("seq.mid", "seq.flac")
        #s = fs.midi_to_audio("seq.mid", "seq" .wav")
        os.remove("seq.mid")
        return s

    def get_image(self, path):
        st = stream.Stream()
        st.append(self.tkey)
        st.append(self.key_sign)
        for i in self.seq_pitches:
            st.append(note.Note(i))
        st.write("musicxml.png", fp=path + "/" + nice_name(self.seq_pitches) + ".png")
        os.remove(path + "/" + nice_name(self.seq_pitches) + ".musicxml")
        os.rename(path + "/" + nice_name(self.seq_pitches) + "-1.png", path + "/" + nice_name(self.seq_pitches) + ".png")









