from Tools import get_lst
import os
from datetime import datetime


def clear_RSeqBank():
    for i in get_lst("secuencias/Rítmicas/", True, False):
        for j in get_lst("secuencias/Rítmicas/" + i, True, False):
            for k in get_lst("secuencias/Rítmicas/" + i + "/" + j, True, False):
                for m in get_lst("secuencias/Rítmicas/" + i + "/" + j + "/" + k, False, False):
                    os.remove("secuencias/Rítmicas/" + i + "/" + j + "/" + k + "/" + m)




a = input("Queres borrar el banco de secuencias rítmicas. y/n")
if a == "y":
    start_time = datetime.now()
    clear_RSeqBank()
    end_time = datetime.now()
    print("Borrado")
    print('Duration: {}'.format(end_time - start_time))
else:
    print("No borramos nada.... ojo con lo que tipeas")