from RSeqClass import *
from Tools import get_lst
from datetime import datetime


def get_seq_bank(cuantas):
    for i in get_lst("secuencias/Rítmicas", True, False):
        for j in get_lst("secuencias/Rítmicas/" + i, True, False):
            for k in get_lst("secuencias/Rítmicas/" + i + "/" + j, True, False):
                for m in range(cuantas):
                    print("lvl " + i + j + " pulsos " + k + " " + str(m))
                    s = Rsequence(int(j), i, int(k))
                    s.get_image("secuencias/Rítmicas/" + i + "/" + j + "/" + k)
                    s.get_seq_audio("secuencias/Rítmicas/" + i + "/" + j + "/" + k)


n = int(input("Cuantas secuencias por categoria?"))
start_time = datetime.now()
get_seq_bank(n)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))