import sys
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt


# Attēlo joslu diagrammu, kas blakus salīdzina divu rakstu emocijas.
# emocijas1 un emocijas2 ir dict {emocija: varbūtība} - tieši tādi, ko atgriež
# EmocijuAnalize.analizet_emocijas(). Vēlāk, kad dati nāks no datubāzes,
# vajadzēs vienkārši tos no turienes ielādēt šajā pašā formātā.
# Grafiks tiek saglabāts kā attēls un atvērts ar OS noklusēto skatītāju, jo
# matplotlib interaktīvais logs ne visur strādā (piem. bez tkinter).
def attelot_emociju_salidzinajumu(emocijas1, emocijas2, nosaukums1="1. raksts", nosaukums2="2. raksts", fails="grafiks.png"):
    emocijas = list(emocijas1.keys())
    vertibas1 = [emocijas1[e] for e in emocijas]
    vertibas2 = [emocijas2[e] for e in emocijas]

    x = np.arange(len(emocijas))
    platums = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - platums / 2, vertibas1, platums, label=nosaukums1)
    ax.bar(x + platums / 2, vertibas2, platums, label=nosaukums2)

    ax.set_ylabel("Varbūtība")
    ax.set_title("Emociju salīdzinājums")
    ax.set_xticks(x)
    ax.set_xticklabels(emocijas)
    ax.legend()

    plt.tight_layout()
    plt.savefig(fails)
    plt.close(fig)

    print(f"Grafiks saglabāts: {fails}")
    atvert_failu(fails)


# Atver failu ar operētājsistēmas noklusēto programmu.
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
