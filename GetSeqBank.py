from SeqClass import Sequence, nice_name
from Tools import get_lst
from datetime import datetime


def get_seq_bank(n, ext, bool):
    for root in get_lst("secuencias/Melódicas", True, False):
        for mode in get_lst("secuencias/Melódicas" + "/" + root, True, False):
            for sounds in get_lst("secuencias/Melódicas" + "/" + root + "/" + mode, True, False):
                if bool == "y":
                    if int(sounds) == 3:
                        for i in range(n):
                            s = Sequence(root, mode, int(sounds), "True")
                            s.get_seq_audio_bank("secuencias/Melódicas" + "/" + root + "/" + mode + "/" + sounds,
                                                 nice_name(s.seq_pitches), ext)
                            s.get_image("secuencias/Melódicas" + "/" + root + "/" + mode + "/" + sounds)
                else:
                    if int(sounds) < 6:
                        for i in range(n):
                            s = Sequence(root, mode, int(sounds), "True")
                            s.get_seq_audio_bank("secuencias/Melódicas" + "/" + root + "/" + mode + "/" + sounds,
                                                 nice_name(s.seq_pitches), ext)
                            s.get_image("secuencias/Melódicas" + "/" + root + "/" + mode + "/" + sounds)
                    else:
                        for i in range(n):
                            s = Sequence(root, mode, int(sounds), "False")
                            s.get_seq_audio_bank("secuencias/Melódicas" + "/" + root + "/" + mode + "/" + sounds,
                                                 nice_name(s.seq_pitches), ext)
                            s.get_image("secuencias/Melódicas" + "/" + root + "/" + mode + "/" + sounds)


e = input("midi o audio?")
f = input("Solo secuencias de tres sonidos? y/n")
i = int(input("Cuantas secuencias por categoria?"))
start_time = datetime.now()
get_seq_bank(i, e, f)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))