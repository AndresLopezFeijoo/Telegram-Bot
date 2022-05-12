from datetime import date
import json
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from collections import Counter

def new_json_data(entry):
    with open("usage.json", "r") as file:
        data = json.load(file)
        if list(data.keys())[-1] == date.today().strftime("%d/%m/%y"):
            data[date.today().strftime("%d/%m/%y")].append(entry)
        else:
            data[date.today().strftime("%d/%m/%y")] = [entry]
    with open("usage.json", "w") as file:
        json.dump(data, file, separators=(",", ":"), indent = 3)


def plot_data(dict): # El json de uso del bot
    categories = ["dm", "dr", "lm", "lr", "sm", "sr", "bib", "sol", "hind", "melo", "rec"]
    dates = []
    total = []
    dm = []
    dr = []
    lm = []
    lr = []
    sm = []
    sr = []
    bib = []
    sol = []
    hind = []
    melo = []
    rec = []
    for i in dict:
        dates.append(i)
        counter = Counter()
        counter.update(dict[i])
        for j in categories:
            if j not in counter:
                eval(j).append(0)
            else:
                eval(j).append(counter[j])
    for i, j, k, l, m, n, o, p, q, r, s in zip(dm, dr, lm, lr, sm, sr, bib, sol, hind, melo, rec):
        total.append(i + j + k + l + m + n + o + p + q + r + s)
    x_ind = np.arange(len(dates))
    width = 0.025
    plt.plot(x_ind, total, label = "totales")
    plt.bar(x_ind + width/2, dm, width = width, label = "Dict. Mel")
    plt.bar(x_ind - width/2, dr, width = width, label = "Dict. Rit")
    plt.bar(x_ind + 1.5*width, lm, width = width, label = "Lect. Mel.")
    plt.bar(x_ind - 1.5*width, lr, width = width, label = "Lect. Rit")
    plt.bar(x_ind + 2.5*width, sm, width = width, label = "Sec. Mel.")
    plt.bar(x_ind - 2.5*width, sr, width = width, label = "Sec. Rit")
    plt.bar(x_ind + 3.5 * width, bib, width=width, label="Biblio")
    plt.bar(x_ind - 3.5 * width, sol, width=width, label="Solfeo")
    plt.bar(x_ind + 4.5 * width, hind, width=width, label="Hindemith")
    plt.bar(x_ind - 4.5 * width, melo, width=width, label="Melo Cast.")
    plt.bar(x_ind - 5.5 * width, melo, width=width, label="Recon")

    plt.title("Uso diario de Astorito") #Titulo
    plt.legend()  #Muestra las referencias de "label"
    plt.xticks(ticks=x_ind, labels=dates) # cambia los labels de x para que no sean los numeros que cree para mover las barras
    plt.grid(ls = "--")
    plt.locator_params(axis = "x",tight = True, nbins = 12) # Solo va a mostrar nbins ticks en el eje X
    #plt.show()
    plt.gcf().autofmt_xdate() # Inclina las fechas
    plt.savefig("grafico_uso.png")
    plt.close()

