from SeqClass import Sequence, nice_name
from Tools import get_lst
from datetime import datetime

def get_seq_bank(n, ext):
    for i in get_lst("secuencias", True):
        for j in get_lst("secuencias/" + i, True):
            for k in get_lst("secuencias/" + i + "/" + j, True):
                if int(k) < 6:
                    for m in range(n):
                        s = Sequence(i, j, int(k), "True")
                        s.get_seq_audio_bank("secuencias/" + i + "/" + j + "/" + k, nice_name(s.seq_pitches), ext)
                else:
                    for m in range(n):
                        s = Sequence(i, j, int(k), "False")
                        s.get_seq_audio_bank("secuencias/" + i + "/" + j + "/" + k, nice_name(s.seq_pitches), ext)


e = input("midi o audio?")
i = int(input("Cuantas secuencias por categoria?"))
start_time = datetime.now()
get_seq_bank(i, e)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))