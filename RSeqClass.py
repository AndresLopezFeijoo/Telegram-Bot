from music21 import *
import random as rd
from midi2audio import FluidSynth
import os

figures = {0: note.Note("f5", quarterLength=3), 1: note.Rest("f5", quarterLength=3),
           2: note.Note("f5", quarterLength=2), 3: note.Rest("f5", quarterLength=2),
           4: note.Note("f5", quarterLength=1.5), 5: note.Rest("f5", quarterLength=1.5),
           6: note.Note("f5", quarterLength=1), 7: note.Rest("f5", quarterLength=1),
           8: note.Note("f5", quarterLength=0.75), 9: note.Rest("f5", quarterLength=0.75),
           10: note.Note("f5", quarterLength=0.5), 11: note.Rest("f5", quarterLength=0.5),
           12: note.Note("f5", quarterLength=0.33), 13: note.Note("f5", quarterLength=0.2),
           14: note.Note("f5", quarterLength=0.375), 15: note.Rest("f5", quarterLength=0.375),
           16: note.Note("f5", quarterLength=0.25), 17: note.Rest("f5", quarterLength=0.25),
           18: note.Note("f5", quarterLength=0.142), 19: note.Rest("f5", quarterLength=0.33),
           20: note.Rest("f5", quarterLength=0.2), 21: note.Rest("f5", quarterLength=0.142),
           22: note.Note("f5", quarterLength=0.125), 23: note.Rest("f5", quarterLength=0.125)}

# A partir de la 24 son con fusas
cells = {"binario": {0: [0], 1: [6], 2: [7], 3: [10, 10], 4: [11, 10], 5: [10, 11], 6: [16, 16, 10], 7: [10, 16, 16],
               8: [16, 16, 11], 9: [11, 16, 16], 10: [17, 16, 10], 11: [10, 17, 16], 12: [16, 10, 16],
               13: [16, 11, 16], 14: [8, 16], 15: [16, 8], 16: [17, 8], 17: [12, 12, 12], 18: [10, 6, 10],
               19: [11, 6, 10],
               20: [10, 4], 21: [16, 16, 4], 22: [4, 16, 16], 23: [11, 4], 24: (8, 16), 25: (9, 16), 26: (10, 10),
               27: (10, 11),
               28: (11, 10), 29: (16, 8), 30: (17, 8), 31: (8, 22, 22), 32: (9, 22, 22), 33: (10, 16, 16),
               34: (11, 16, 16), 35: (16, 10, 16), 36: (16, 11, 16), 37: (16, 16, 10), 38: (16, 16, 11),
               39: (17, 10, 16),
               40: (17, 16, 10), 41: (22, 22, 8), 42: (22, 22, 9), 43: (23, 22, 8), 44: (10, 16, 22, 22),
               45: (10, 22, 16, 22), 46: (10, 22, 22, 16), 47: (10, 22, 22, 17), 48: (11, 16, 22, 22),
               49: (11, 22, 16, 22), 50: (11, 22, 22, 16), 51: (16, 10, 22, 22), 52: (16, 11, 22, 22),
               53: (16, 16, 16, 16), 54: (16, 16, 16, 17), 55: (16, 16, 17, 16), 56: (16, 17, 16, 16),
               57: (16, 22, 22, 10), 58: (16, 22, 22, 11), 59: (17, 10, 22, 22), 60: (17, 16, 16, 16),
               61: (17, 22, 22, 10), 62: (22, 16, 22, 10), 63: (22, 16, 22, 11), 64: (22, 22, 10, 16),
               65: (22, 22, 11, 16), 66: (22, 22, 16, 10), 67: (22, 22, 16, 11), 68: (22, 22, 17, 10),
               69: (10, 22, 22, 22, 22), 70: (10, 22, 22, 22, 23), 71: (10, 22, 22, 23, 22), 72: (10, 22, 23, 22, 22),
               73: (10, 23, 22, 22, 22), 74: (11, 22, 22, 22, 22), 75: (16, 16, 16, 22, 22), 76: (16, 16, 17, 22, 22),
               77: (16, 16, 22, 16, 22), 78: (16, 16, 22, 22, 16), 79: (16, 16, 22, 22, 17), 80: (16, 17, 16, 22, 22),
               81: (16, 17, 22, 16, 22), 82: (16, 17, 22, 22, 16), 83: (16, 22, 16, 16, 22), 84: (16, 22, 16, 22, 16),
               85: (16, 22, 22, 16, 16), 86: (16, 22, 22, 16, 17), 87: (16, 22, 22, 17, 16), 88: (17, 16, 16, 22, 22),
               89: (17, 16, 22, 16, 22), 90: (17, 16, 22, 22, 16), 91: (17, 22, 16, 16, 22), 92: (17, 22, 16, 22, 16),
               93: (17, 22, 22, 16, 16), 94: (22, 10, 22, 22, 22), 95: (22, 11, 22, 22, 22), 96: (22, 16, 16, 16, 22),
               97: (22, 16, 16, 16, 23), 98: (22, 16, 16, 22, 16), 99: (22, 16, 22, 16, 16), 100: (22, 16, 22, 16, 17),
               101: (22, 16, 22, 17, 16), 102: (22, 22, 10, 22, 22), 103: (22, 22, 11, 22, 22),
               104: (22, 22, 16, 16, 16),
               105: (22, 22, 16, 16, 17), 106: (22, 22, 16, 17, 16), 107: (22, 22, 17, 16, 16),
               108: (22, 22, 22, 10, 22),
               109: (22, 22, 22, 22, 10), 110: (22, 22, 22, 22, 11), 111: (23, 10, 22, 22, 22),
               112: (23, 16, 16, 16, 22),
               113: (23, 16, 16, 22, 16), 114: (23, 16, 22, 16, 16), 115: (23, 22, 10, 22, 22),
               116: (23, 22, 16, 16, 16),
               117: (16, 16, 22, 22, 22, 22), 118: (16, 16, 23, 22, 22, 22), 119: (16, 17, 22, 22, 22, 22),
               120: (16, 22, 16, 22, 22, 22), 121: (16, 22, 22, 16, 22, 22), 122: (16, 22, 22, 17, 22, 22),
               123: (16, 22, 22, 22, 16, 22), 124: (16, 22, 22, 22, 22, 16), 125: (16, 22, 22, 22, 22, 17),
               126: (17, 16, 22, 22, 22, 22), 127: (17, 22, 16, 22, 22, 22), 128: (17, 22, 22, 16, 22, 22),
               129: (17, 22, 22, 22, 16, 22), 130: (17, 22, 22, 22, 22, 16), 131: (22, 16, 16, 22, 22, 22),
               132: (22, 16, 22, 16, 22, 22), 133: (22, 16, 22, 22, 16, 22), 134: (22, 16, 22, 22, 22, 16),
               135: (22, 16, 22, 23, 16, 22), 136: (22, 16, 22, 23, 22, 16), 137: (22, 22, 16, 16, 22, 22),
               138: (22, 22, 16, 22, 16, 22), 139: (22, 22, 16, 22, 22, 16), 140: (22, 22, 16, 22, 22, 17),
               141: (22, 22, 16, 23, 16, 22), 142: (22, 22, 16, 23, 22, 16), 143: (22, 22, 17, 16, 22, 22),
               144: (22, 22, 17, 22, 16, 22), 145: (22, 22, 17, 22, 22, 16), 146: (22, 22, 22, 16, 16, 22),
               147: (22, 22, 22, 16, 22, 16), 148: (22, 22, 22, 22, 16, 16), 149: (22, 22, 22, 22, 17, 16),
               150: (23, 16, 16, 22, 22, 22), 151: (23, 16, 22, 16, 22, 22), 152: (23, 16, 22, 22, 16, 22),
               153: (23, 16, 22, 22, 22, 16), 154: (23, 22, 16, 22, 16, 22), 155: (23, 22, 16, 22, 22, 16),
               156: (23, 22, 22, 22, 16, 16), 157: (16, 22, 22, 22, 22, 22, 22), 158: (16, 22, 22, 22, 22, 23, 22),
               159: (16, 22, 22, 23, 22, 22, 22), 160: (16, 23, 22, 22, 22, 22, 22), 161: (17, 22, 22, 22, 22, 22, 22),
               162: (22, 16, 22, 22, 22, 22, 22), 163: (22, 17, 22, 22, 22, 22, 22), 164: (22, 22, 16, 22, 22, 22, 22),
               165: (22, 22, 17, 22, 22, 22, 22), 166: (22, 22, 22, 16, 22, 22, 22), 167: (22, 22, 22, 22, 16, 22, 22),
               168: (22, 22, 22, 22, 17, 22, 22), 169: (22, 22, 22, 22, 22, 16, 22), 170: (22, 22, 22, 22, 22, 22, 16),
               171: (22, 22, 22, 22, 22, 22, 17), 172: (22, 22, 22, 22, 23, 16, 22), 173: (22, 22, 22, 22, 23, 22, 16),
               174: (22, 22, 22, 23, 16, 22, 22), 175: (22, 22, 22, 23, 22, 16, 22), 176: (22, 22, 22, 23, 22, 22, 16),
               177: (23, 16, 22, 22, 22, 22, 22), 178: (23, 22, 22, 22, 16, 22, 22), 179: (23, 22, 22, 22, 22, 16, 22),
               180: (23, 22, 22, 22, 22, 22, 16), 181: (22, 22, 22, 22, 22, 22, 22, 22),
               182: (22, 22, 22, 22, 22, 22, 23, 22), 183: (22, 22, 22, 22, 23, 22, 22, 22),
               184: (22, 22, 23, 22, 22, 22, 22, 22), 185: (23, 22, 22, 22, 22, 22, 22, 22), 186: [6]},
         "ternario": {1: [1.5], 2: [0.5, 0.5, 0.5], 3: [1, 0.5], 4: [0.25, 0.25, 0.5, 0.5]}}

lvl_num = {"binario": {0: [0, 23], 1: [24, 185], 2: [186]}, "ternario": {0: [], 1: [], 2: []}}

names = {"quarter": "Negra", "eighth": "Corchea", "16th": "Semi", "half": "Blanca", "32nd": "Fusa",
         "Silencio de quarter": "Silencio de Negra", "Silencio de eighth": "Silencio de corchea",
         "Silencio de 16th": "Silencio de Semi", "Silencio de half": "Silencio de Blanca",
         "Silencio de 32nd": "Silencio de Fusa"}



class Rsequence:

    def __init__(self, lvl, pie, pulses):
        self.level = lvl  # nivel en nros
        self.pie = pie  # binario ternario
        self.pulses = pulses  # cantidad de pulsos
        self.num = self.get_num  # numerador
        self.tkey = meter.TimeSignature(self.get_num() + "/" + self.get_den())  # indicacion de compas
        self.clef = clef.PercussionClef()  # clave de percusion
        self.sequence = self.create_seq()

    def get_num(self):
        if self.pie == "binario":
            return str(self.pulses)
        else:
            return str(self.pulses * 3)

    def get_den(self):
        if self.pie == "binario":
            return "4"
        else:
            return "8"


    def cell_list_lvl(self):  # lista de celulas segun nivel
        nr = self.pulses//2
        lst = []
        if self.level == 1:
            while len(lst) < self.pulses:
                lst.append(rd.randint(0, 23))

        elif self.level == 2:
            while len(lst) < self.pulses - nr:
                lst.append(rd.randint(0, 23))
            while len(lst) < self.pulses:
                lst.append(rd.randint(24, 185))

        elif self.level == 3:
            while len(lst) < self.pulses - nr:
                lst.append(rd.randint(0, 23))
            while len(lst) < self.pulses - (nr//2):
                lst.append(rd.randint(24, 184))
            while len(lst) < self.pulses:
                lst.append(rd.randint(186, 186))

        rd.shuffle(lst)
        return lst

    def create_seq(self):
        s = stream.Stream()
        tpo = tempo.MetronomeMark(number=80)
        s.append(tpo)
        s.append(self.tkey)
        s.append(self.clef)
        s.staffLines = 1

        while s.quarterLength < self.pulses:
            for i in self.cell_list_lvl():
                for j in cells[self.pie][i]:
                    s.repeatAppend(figures[j], 1)
                while s.quarterLength > self.pulses:
                    s.pop(0)

        return s






    #def __init__(self, nr, year, den):
    #    self.number = nr
    #    self.year = year
    #    self.den = den
    #    self.tkey = meter.TimeSignature(str(self.number) + "/" + self.den)
    #    self.clef = clef.PercussionClef()
    #    self.sequence = self.create_seq()
    #    self.figures = self.figure_names()
    #    self.spfigures = self.sp_names()

    #def create_seq(self):
    #    s = stream.Stream()
    #    tpo = tempo.MetronomeMark(number=80)
    #    s.append(tpo)
    #    s.append(self.tkey)
    #    s.append(self.clef)
    #    s.staffLines = 1
    #    while s.quarterLength < self.number:
    #        if self.cheat != 0:
    #            nr = self.cheat
    #        else:
    #            nr = rd.randint(1, 184)
    #        if nr < 4:
    #            s.repeatAppend(figures[nr], 1)
    #        else:
    #            for i in cells[str(self.tkey.ratioString)[-1]][nr]:
    #                s.repeatAppend(figures[i], 1)
    #        while s.quarterLength > self.number:
    #            s.pop(0)
     #   return s

    #def figure_names(self):
     #   nm = []
      #  for i in list(self.sequence.elements[4:]):
       #     if i.isRest:
        #        nm.append("Silencio de " + i.duration.type + ", ")
         #   else:
          #      nm.append(i.duration.type + ", ")
        #return nm

    #def sp_names(self):
     #   sp_names = ""
      #  for i in self.figures:
       #     sp_names += names[i[:-2]] + ", "
        #return sp_names[:-2]

    #def get_seq_audio(self, path, name, ext):
     #   print(path + "--" + name)
      #  self.sequence.write("midi", path + "/" + name + ".mid")
       # if ext == "audio":
        #    fs = FluidSynth()
         #   fs.midi_to_audio(path + "/" + name + ".mid", path + "/" + name + ".flac")
          #  os.remove(path + "/" + name + ".mid")

    #def export(self, path, *args):  # Args = nombre del archivo para los png
        # self.create_seq().write('musicxml', fp=path + "/" + str(self.spfigures) + ".xml")
        # self.create_seq().write("musicxml.pdf", fp=path + "/" + str(self.spfigures) + ".pdf")
     #   self.sequence.write("musicxml.png", fp=path + "/" + str(args) + ".png")



r = Rsequence(2, "binario", 3)
r.sequence.show()
#0, 1, 2a = Rsequence(4, "I", "4", 0)
#a.sequence.show()
# print(a.cheat)
# a.export("secuencias/ritmicas")
# a.sequence.write("musicxml.png", fp="secuencias/ritmicas/ap.png")
# for i in cells2["4"]:
#    a = Rcheatsequence(1, "I", "4", i)
#    #a.sequence.show()
#    #print(a.figures)
#    #print(a.spfigures)
#    a.export("secuencias/ritmicas/a")
#    a.get_seq_audio("secuencias/ritmicas/b", a.sp_names(), "audio")
