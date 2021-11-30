from Tools import get_lst
import os
from datetime import datetime


def clear_seq_bank(type):
    for i in get_lst("secuencias", True):
        for j in get_lst("secuencias/" + i, True):
            for k in get_lst("secuencias/" + i + "/" + j, True):
                for m in get_lst("secuencias/" + i + "/" + j + "/" + k, False):
                    if type == "All":
                        os.remove(os.path.join("secuencias/" + i + "/" + j + "/" + k, m))
                    elif m.endswith(type):
                        print("Borrando: " + m)
                        os.remove(os.path.join("secuencias/" + i + "/" + j + "/" + k, m))




a = input("Queres borrar el banco de secuencias. y/n")
b = input("Que tipo de archivo? .mid/.flac/All")
if a == "y":
    start_time = datetime.now()
    clear_seq_bank(b)
    end_time = datetime.now()
    print("Borrado")
    print('Duration: {}'.format(end_time - start_time))
else:
    print("No borramos nada.... ojo con lo que tipeas")