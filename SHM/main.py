from jetson_stats import jtop
import time

# Créer une instance de jtop
with jtop() as jetson:
    # Boucle infinie pour afficher les stats
    while True:
        # Effacer la sortie précédente
        print("\033[H\033[J", end="")

        # Afficher les stats de CPU
        print("CPU stats:")
        for core in jetson.cpu:
            print(f"Core {core['core']} usage: {core['val']}%")

        # Afficher les stats de mémoire
        print("\nMemory stats:")
        print(f"Used memory: {jetson.ram['use'] / 1024:.2f} GB")
        print(f"Total memory: {jetson.ram['tot'] / 1024:.2f} GB")

        # Attendre avant la prochaine mise à jour
        time.sleep(5)
