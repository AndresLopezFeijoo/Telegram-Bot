from music21 import *
import random as rd
from midi2audio import FluidSynth
import os
from pydub import AudioSegment

# A partir de la 24 son con fusas, A patir del 186 tresillos con silencios y semis, del 201 son quintillos con silencio
cells = {"Binario": {0: [0], 1: [6], 2: [7], 3: [10, 10], 4: [11, 10], 5: [10, 11], 6: [16, 16, 10], 7: [10, 16, 16],
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
               184: (22, 22, 23, 22, 22, 22, 22, 22), 185: (23, 22, 22, 22, 22, 22, 22, 22), 186: (12, 12),
               187: (19, 12), 188: (12, 12, 12), 189: (12, 12, 19), 190: (12, 19, 12), 191: (24, 24, 12, 12),
               192: (19, 12, 12), 193: (12, 12, 24, 24), 194: (12, 24, 24, 12), 195: (12, 24, 24, 19),
               196: (19, 12, 24, 24), 197: (19, 24, 24, 12), 198: (12, 24, 24, 24, 24), 199: (19, 24, 24, 24, 24),
               200: (24, 24, 24, 24, 24, 24), 201: (13, 13, 13, 13, 13), 202: (20, 13, 13, 13, 13),
               203: (13, 20, 13, 13, 13), 204: (13, 13, 20, 13, 13), 205: (13, 13, 13, 20, 13),
               206: (13, 13, 13, 13, 20)},
         "Ternario": {0: (6, 10), 1: (6, 11), 2: (7, 10), 3: (10, 6), 4: (10, 7), 5: (11, 6), 6: (6, 16, 16),
                      7: (6, 17, 16), 8: (7, 16, 16), 9: (10, 10, 10), 10: (10, 10, 11), 11: (10, 11, 10),
                      12: (11, 10, 10), 13: (16, 6, 16), 14: (16, 16, 6), 15: (16, 16, 7), 16: (17, 16, 6),
                      17: (10, 10, 16, 16), 18: (10, 11, 16, 16), 19: (10, 16, 10, 16), 20: (10, 16, 16, 10),
                      21: (10, 16, 16, 11), 22: (10, 17, 10, 16), 23: (10, 17, 16, 10), 24: (11, 10, 16, 16),
                      25: (11, 16, 10, 16), 26: (11, 16, 16, 10), 27: (16, 10, 10, 16), 28: (16, 10, 16, 10),
                      29: (16, 16, 10, 10), 30: (16, 16, 10, 11), 31: (16, 16, 11, 10), 32: (17, 10, 10, 16),
                      33: (17, 16, 10, 10), 34: (10, 16, 16, 16, 16), 35: (10, 17, 16, 16, 16),
                      36: (11, 16, 16, 16, 16), 37: (16, 10, 16, 16, 16), 38: (16, 16, 10, 16, 16),
                      39: (16, 16, 11, 16, 16), 40: (16, 16, 16, 10, 16), 41: (16, 16, 16, 16, 10),
                      42: (16, 16, 16, 16, 11), 43: (16, 16, 17, 10, 16), 44: (16, 16, 17, 16, 10),
                      45: (17, 10, 16, 16, 16), 46: (17, 16, 10, 16, 16), 47: (17, 16, 16, 10, 16),
                      48: (17, 16, 16, 16, 10), 49: (16, 16, 16, 16, 16, 16), 50: (17, 16, 16, 16, 16, 16),
                      51: (10, 10, 22, 22, 22, 22), 52: (10, 10, 23, 22, 22, 22), 53: (10, 11, 22, 22, 22, 22), # A partir del 52 con semis
                      54: (10, 22, 10, 22, 22, 22), 55: (10, 22, 22, 10, 22, 22), 56: (10, 22, 22, 10, 22, 23),
                      57: (10, 22, 22, 11, 22, 22), 58: (10, 22, 22, 22, 10, 22), 59: (10, 22, 22, 22, 22, 10),
                      60: (10, 22, 22, 22, 22, 11), 61: (10, 22, 22, 22, 23, 10), 62: (10, 23, 10, 22, 22, 22),
                      63: (10, 23, 22, 10, 22, 22), 64: (10, 23, 22, 22, 10, 22), 65: (10, 23, 22, 22, 22, 10),
                      66: (11, 10, 22, 22, 22, 22), 67: (11, 22, 10, 22, 22, 22), 68: (11, 22, 22, 10, 22, 22),
                      69: (11, 22, 22, 22, 10, 22), 70: (11, 22, 22, 22, 22, 10), 71: (22, 22, 10, 10, 22, 22),
                      72: (22, 22, 10, 22, 22, 10), 73: (22, 22, 10, 22, 22, 11), 74: (22, 22, 22, 10, 10, 22),
                      75: (22, 22, 22, 10, 11, 22), 76: (22, 22, 22, 10, 22, 10), 77: (22, 22, 22, 22, 10, 10),
                      78: (22, 22, 22, 22, 10, 11), 79: (22, 22, 22, 22, 11, 10), 80: (22, 22, 22, 23, 10, 10),
                      81: (23, 22, 10, 10, 22, 22), 82: (23, 22, 10, 22, 10, 22), 83: (23, 22, 22, 22, 10, 10),
                      84: (25, 25, 25, 25), 85: (27, 27, 27, 27, 27), 86: (29, 29, 29, 29, 29, 29, 29)}}  # A partir del 84 cuatrillo quintillo y septisillo





class Rsequence:

    def __init__(self, lvl, pie, pulses):
        self.level = lvl  # nivel en nros
        self.pie = pie  # binario ternario
        self.pulses = pulses  # cantidad de pulsos
        self.num = self.get_num  # numerador
        self.tkey = meter.TimeSignature(self.get_num() + "/" + self.get_den())  # indicacion de compas
        self.clef = clef.PercussionClef()  # clave de percusion
        self.quarterlength = self.get_quarterlength()
        self.length = 0
        self.cell_lst = self.cell_list_lvl()
        self.sequence = self.create_seq()
        self.name = self.get_name()

    def get_quarterlength(self):
        if self.pie == "Binario":
            return self.pulses
        else:
            return self.pulses * 1.5

    def get_num(self):
        if self.pie == "Binario":
            if self.pulses == 6:
                return str(round(self.pulses/2))
            else:
                return str(self.pulses)
        else:
            return str(self.pulses * 3)

    def get_den(self):
        if self.pie == "Binario":
            return "4"
        else:
            return "8"

    def counter(self, *args):
        values = {0: 3, 1: 3, 2: 2, 3: 2, 4: 1.5, 5: 1.5, 6: 1, 7: 1, 8: 3 / 4, 9: 3 / 4, 10: 1 / 2, 11: 1 / 2,
                  12: 1 / 3,
                  13: 1 / 5, 14: 3 / 8, 15: 3 / 8, 16: 1 / 4, 17: 1 / 4, 18: 1 / 7, 19: 1 / 3, 20: 1 / 5, 21: 1 / 7,
                  22: 1 / 8, 23: 1 / 8,
                  24: 1 / 6, 25: 1.5 / 4, 26: 1.5 / 4, 27: 1.5 / 5, 28: 1.5 / 5, 29: 1.5 / 7, 30: 1.5 / 7}
        for i in cells[self.pie][args[0]]:
            self.length += values[i]

    def pulse_voice(self):
        p = stream.Voice()
        #tpo = tempo.MetronomeMark("slow")
        #i = instrument.BassDrum()
        #p.append(tpo)
        #p.append(self.tkey)
        #p.append(self.clef)
        #p.staffLines = 1
        #p.append(i)
        for j in range(self.pulses):
            n2 = note.Note("a4", quarterLength=self.quarterlength/self.pulses)
            n2.stemDirection = "down"
            p.repeatAppend(n2, 1)
        return p


    def get_note(self, n):
        note_data = {0: [1, "half", 0, 1, 1, 3],  # Blanca con punto
                     1: [0, "half", 1, 1, 1, 3],  # Silencio Blanca con punto
                     2: [1, "half", 0, 1, 1, 2],  # Blanca
                     3: [0, "half", 0, 1, 1, 2],  # Sil de Blanca
                     4: [1, "quarter", 1, 1, 1, 1.5],  # Negra con punto
                     5: [0, "quarter", 1, 1, 1, 1.5],  # Sil de negra con punto
                     6: [1, "quarter", 0, 1, 1, 1],  # Negra
                     7: [0, "quarter", 0, 1, 1, 1],  # Sil de Negra
                     8: [1, "eighth", 1, 1, 1, 3 / 4],  # Corchea con punto
                     9: [0, "eighth", 1, 1, 1, 3 / 4],  # Sil de Corchea con punto
                     10: [1, "eighth", 0, 1, 1, 1 / 2],  # Corchea
                     11: [0, "eighth", 0, 1, 1, 1 / 2],  # Sil de Corchea
                     12: [1, "eighth", 0, 3, 2, 1 / 3],  # Corchea de Tresillo
                     13: [1, "16th", 0, 5, 4, 1 / 5],  # Semi de Quintillo
                     14: [1, "16th", 1, 1, 1, 3 / 8],  # Semi con punto
                     15: [0, "16th", 1, 1, 1, 3 / 8],  # Sil de semi con punto
                     16: [1, "16th", 0, 1, 1, 1 / 4],  # Semi
                     17: [0, "16th", 0, 1, 1, 1 / 4],  # Sil de Semi
                     18: [1, "16th", 0, 7, 4, 1 / 7],  # Semi de septisillo
                     19: [0, "eighth", 0, 3, 2, 1 / 3],  # Sil de Corche de Tresillo
                     20: [0, "16th", 0, 5, 4, 1 / 5],  # Sil de semi de quintillo
                     21: [0, "16th", 0, 7, 4, 1 / 7],  # Sil de semi de septisillo
                     22: [1, "32nd", 0, 1, 1, 1 / 8],  # Fusa
                     23: [0, "32nd", 0, 1, 1, 1 / 8],  # Sil de Fusa
                     24: [1, "16th", 0, 6, 4, 1 / 6],  # Semi de Seisillo
                     25: [1, "eighth", 0, 4, 3, 1.5 / 4],  # Corchea de Cuatrillo CC
                     26: [0, "eighth", 0, 4, 3, 1.5 / 4],  # Sil de Corche de Cuatrillo CC
                     27: [1, "eighth", 0, 5, 3, 0],  # Corchea de Quintillo CC
                     28: [0, "eighth", 0, 5, 3, 0],  # Sil de Corchea de Qintillo CC
                     29: [1, "16th", 0, 7, 6, 0],  # Semi de Septisillo CC
                     30: [0, "16th", 0, 7, 6, 0]}  # Sil de Semi de Septisillo CC
        if note_data[n][0] == 0:
            a = note.Rest()
        if note_data[n][0] == 1:
            a = note.Note("e5")
        a.duration.type = note_data[n][1]
        a.duration.dots = note_data[n][2]
        t = duration.Tuplet(note_data[n][3], note_data[n][4])
        a.duration.appendTuplet(t)
        if self.pie == "binario":
            a.quarterLength = note_data[n][5]
        return a


    def cell_list_lvl(self):  # lista de celulas segun nivel
        lvl_num = {"Binario": {1: [0, 23], 2: [24, 185], 3: [186, 206]},
                   "Ternario": {1: [0, 50], 2: [51, 83], 3: [84, 86]}}
        while round(self.length, 2) != self.quarterlength:
            nota = False  # Indica si la secuencia empieza con una nota. False = empieza con silencio
            while nota is False:
                lst = []
                self.length = 0
                if self.level == 1:
                    while round(self.length, 2) < self.quarterlength:
                        n = rd.randint(lvl_num[self.pie][self.level][0], lvl_num[self.pie][self.level][1])
                        lst.append(n)
                        self.counter(n)

                elif self.level == 2:
                    while round(self.length, 2) < self.quarterlength//2:
                        n = rd.randint(lvl_num[self.pie][int(self.level) - 1][0], lvl_num[self.pie][int(self.level) - 1][1])
                        lst.append(n)
                        self.counter(n)
                    while round(self.length, 2) < self.quarterlength:
                        n = rd.randint(lvl_num[self.pie][self.level][0], lvl_num[self.pie][self.level][1])
                        lst.append(n)
                        self.counter(n)

                elif self.level == 3:
                    n = rd.randint(lvl_num[self.pie][self.level][0],
                                   lvl_num[self.pie][self.level][1])
                    lst.append(n)
                    self.counter(n)
                    o = rd.randint(lvl_num[self.pie][int(self.level) - 1][0],
                                   lvl_num[self.pie][int(self.level) - 1][1])
                    lst.append(o)
                    self.counter(o)
                    while self.length < self.quarterlength:
                        n = rd.randint(lvl_num[self.pie][int(self.level) - 2][0],
                                       lvl_num[self.pie][int(self.level) - 2][1])
                        lst.append(n)
                        self.counter(n)
                rd.shuffle(lst)
                if self.get_note(cells[self.pie][lst[0]][0]).isNote:
                    nota = True

        return lst


    def create_seq(self):
        s = stream.Stream()
        t = stream.Voice()
        i = instrument.SnareDrum()
        tpo = tempo.MetronomeMark("slow")
        s.append(tpo)
        s.append(self.tkey)
        s.append(self.clef)
        s.staffLines = 4
        s.append(i)

        for i in self.cell_lst:
            for j in cells[self.pie][i]:
                n = self.get_note(j)
                n.stemDirection = "up"
                t.repeatAppend(n, 1)

        s.insert(t)
        s.insert(self.pulse_voice())

        return s

    def get_name(self):
        n = ""
        for i in self.cell_lst:
            n += str(i) + ","
        return n[:-1]

    def get_image(self, path):
        self.sequence.write("musicxml.png", fp=path + "/" + self.name + ".png")
        os.remove(path + "/" + self.name + ".musicxml")
        os.rename(path + "/" + self.name + "-1.png", path + "/" + self.name + ".png")

    def get_seq_audio(self, path):
        self.sequence.write("midi", path + "/" + self.name + ".mid")
        fs = FluidSynth(sound_font="/Users/andreslopezfeijoo/PycharmProjects/Telegram-Bot/sound fonts/FluidR3_GM.sf2")
        fs.midi_to_audio(path + "/" + self.name + ".mid", path + "/" + self.name + ".flac")
        os.remove(path + "/" + self.name + ".mid")



