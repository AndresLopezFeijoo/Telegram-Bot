from music21 import *
import random as rd

cells = {"2/4": {1: [1], 2: [0.5, 0.5], 3: [1, 0.5, 0.5], 4: [0.25, 0.25, 0.25, 0.25]},
         "6/8": {1: [1.5], 2: [0.5, 0.5, 0.5], 3: [1, 0.5], 4: [0.25, 0.25, 0.5, 0.5]}}

class Rsequence:



    def __init__(self, nr, year, den):
        self.number = nr
        self.year = year
        self.den = den
        self.tkey = meter.TimeSignature(str(self.number) + "/" + self.den)
        self.clef = clef.PercussionClef()
        self.sequence = self.create_seq()
        self.figures = self.figure_names()


    def create_seq(self):
        s = stream.Stream()
        s.append(self.tkey)
        s.append(self.clef)
        s.staffLines =1
        while s.quarterLength < self.number:
            print(s.quarterLength)
            for i in cells[self.tkey.ratioString][rd.randint(1, 4)]:
                n = note.Note("f5", quarterLength=i)
                s.append(n)
        while s.quarterLength > self.number:
            s.pop(0)
        return s

    def figure_names(self):
        names = ""
        for i in self.sequence.getElementsByClass("Note"):
            names += i.duration.type + ", "
        return names[:-2]



a = Rsequence(6, "I", "8")
a.sequence.show()
print(a.figures)


#a.create_cell().show()















#c = note.Note("f5", quarterLength=1.5)
#d = note.Note("f5", quarterLength=0.25)
#e = note.Note("f5", quarterLength=0.75)
#f = note.Note("f5", quarterLength=2)

#s1 = stream.Stream()
#s1.staffLines = 1
#t = meter.TimeSignature("2/4")
#cl = clef.PercussionClef()
#s1.append(t)
#s1.append(cl)
#s1.append(c)
#s1.append(d)
#s2 = stream.Stream()
#s2.append(e)
#s2.append(f)
#s1.append(s2)
#s1.show()


