from music21 import note, scale, stream, pitch
from midi2audio import FluidSynth
import os
import random
import json
import itertools
import timeit

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
        self.n = n #Number of notes in sequence
        self.fund = eval(fund)
        self.scale_names = [str(i) for i in self.m(self.key).getPitches(self.key + "4", self.key + "5")]
        self.scale_pitches = [i for i in self.m(self.key).getPitches(self.key + "4", self.key + "5")]
        self.seq_names = self.fundamental()
        self.seq_pitches = [pitch.Pitch(i) for i in self.seq_names]

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
        #s = fs.midi_to_audio("escala.mid", "escalas/menor armonica/" + n + ".wav")
        os.remove("escala.mid")
        return s

    def get_seq_audio(self):
        st = stream.Stream()
        for i in self.seq_names:
            st.append(note.Note(i, quarterLength=2))
        st.write("midi", "seq.mid")
        start = timeit.default_timer()
        fs = FluidSynth()
        s = fs.midi_to_audio("seq.mid", "seq.flac")
        #s = fs.midi_to_audio("seq.mid", "seq" .wav")
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        os.remove("seq.mid")
        return s

#for i in json.load(open("datos.json"))["roots"]:
#    e = Sequence(i, "Menor armónica", 1, "True")
#    e.get_scale_audio(i)


#e = Sequence("c", "Menor armónica", 1, "True")
#e.get_scale_audio()


