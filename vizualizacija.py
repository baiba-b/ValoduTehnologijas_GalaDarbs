import sys
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Attēlo joslu diagrammu
def attelot_salidzinajumu(grupas, virsraksts="Emociju salīdzinājums", fails="grafiks.png"):
    nosaukumi = list(grupas.keys())
    emocijas = list(next(iter(grupas.values())).keys())

    x = np.arange(len(emocijas))
    platums = 0.8 / len(nosaukumi)

    fig, ax = plt.subplots()

    for i, nosaukums in enumerate(nosaukumi):
        vertibas = [grupas[nosaukums][e] for e in emocijas]
        nobide = (i - (len(nosaukumi) - 1) / 2) * platums
        ax.bar(x + nobide, vertibas, platums, label=nosaukums)

    ax.set_ylabel("Varbūtība")
    ax.set_title(virsraksts)
    ax.set_xticks(x)
    ax.set_xticklabels(emocijas)
    ax.legend()

    plt.tight_layout()
    plt.savefig(fails)
    plt.close(fig)

    print(f"Grafiks saglabāts: {fails}")
    atvert_failu(fails)


# Attēlo vienkāršu joslu diagrammu, sakārtotu dilstoši pēc vērtības
def attelot_neitralitates_rangu(vertibas, virsraksts="Neitralitātes rangs", fails="grafiks.png"):
    sakartots = sorted(vertibas.items(), key=lambda item: item[1], reverse=True)
    nosaukumi = [n for n, _ in sakartots]
    skaitli = [v for _, v in sakartots]

    fig, ax = plt.subplots()
    ax.bar(nosaukumi, skaitli)

    ax.set_ylabel("Vidējā 'neutral' varbūtība")
    ax.set_title(virsraksts)
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    plt.savefig(fails)
    plt.close(fig)

    print(f"Grafiks saglabāts: {fails}")
    atvert_failu(fails)


# Atver failu ar operētājsistēmas noklusēto programmu
def atvert_failu(fails):
    try:
        if sys.platform == "win32":
            os.startfile(fails)
        elif sys.platform == "darwin":
            subprocess.run(["open", fails])
        else:
            subprocess.run(["xdg-open", fails])
    except FileNotFoundError:
        print("Neizdevās automātiski atvērt failu - atver to manuāli.")
