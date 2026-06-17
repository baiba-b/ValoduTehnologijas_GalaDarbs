import numpy as np
import matplotlib.pyplot as plt


# Attēlo joslu diagrammu, kas blakus salīdzina divu rakstu emocijas.
def attelot_emociju_salidzinajumu(emocijas1, emocijas2, nosaukums1="1. raksts", nosaukums2="2. raksts"):
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
    plt.show()
