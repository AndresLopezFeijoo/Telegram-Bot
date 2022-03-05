from Tools import get_lst
import os
from datetime import datetime


def clear_seq_bank(type):
    for i in get_lst("secuencias", True, False):
        for j in get_lst("secuencias/" + i, True, False):
            for k in get_lst("secuencias/" + i + "/" + j, True, False):
                for m in get_lst("secuencias/" + i + "/" + j + "/" + k, False, False):
                    for n in get_lst("secuencias/" + i + "/" + j + "/" + k + "/" + m, False, False):
                        if type == "all":
                            os.remove(os.path.join("secuencias/" + i + "/" + j + "/" + k + "/" + m + "/" + n))
                        elif m.endswith(type):
                            print("Borrando: " + m)
                            os.remove(os.path.join("secuencias/" + i + "/" + j + "/" + k + "/" + m + "/" + n))



a = input("Queres borrar el banco de secuencias melodicas?. y/n")
b = input("Que tipo de archivo? .mid/.flac/all")
if a == "y":
    start_time = datetime.now()
    clear_seq_bank(b)
    end_time = datetime.now()
    print("Borrado")
    print('Duration: {}'.format(end_time - start_time))
else:
    print("No borramos nada.... ojo con lo que tipeas")