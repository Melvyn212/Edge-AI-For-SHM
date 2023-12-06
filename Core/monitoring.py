
import json
import time
import datetime
import subprocess
import os
import threading



def generate_filename():
    base_name = "power_usage_log"
    extension = ".json"
    directory = "tegrastats"
    i = 0

    # Assurez-vous que le dossier existe, sinon créez-le
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construire le chemin du fichier complet
    file_name = f"{directory}/{base_name}_{i}{extension}"

    # Vérifier si le fichier existe et incrémenter l'index si nécessaire
    while os.path.exists(file_name):
        i += 1
        file_name = f"{directory}/{base_name}_{i}{extension}"

    return file_name

import subprocess
import re

def get_tegrastat_data():
    try:
        output = subprocess.check_output(['tegrastat'], text=True)

        # Utilisation de regex pour extraire les données
        ram_usage = re.search(r'RAM (\d+)/(\d+)MB', output)
        cpu_usage = re.search(r'CPU \[(.*?)\]', output)
        gpu_usage = re.search(r'GR3D_FREQ (\d+)%', output)

        if ram_usage and cpu_usage and gpu_usage:
            return {
                'ram_usage': ram_usage.group(1),
                'ram_total': ram_usage.group(2),
                'cpu_usage': cpu_usage.group(1),
                'gpu_usage': gpu_usage.group(1)
            }
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'exécution de tegrastat:", e)

    return None



class DataCollector:
    def __init__(self):
        self.filename = generate_filename()
        self.data_list = []
        self.collecting = False
        self.thread = threading.Thread(target=self.collect_data)

    def start_collecting(self):
        self.collecting = True
        self.thread.start()

    def stop_collecting(self):
        self.collecting = False
        self.thread.join()
        with open(self.filename, 'w') as json_file:
            json.dump(self.data_list, json_file, indent=4)
        print(f"Données enregistrées dans le fichier JSON {self.filename}.")

    def collect_data(self):
        while self.collecting:
            data = get_tegrastat_data()
            data_dict = {
                "time": data[0],
                "power": data[1],
                "cpu_usage": data[2],
                "gpu_usage": data[3]
            }
            self.data_list.append(data_dict)
            time.sleep(1)



# from monitoring import DataCollector

# data_collector = DataCollector()

# data_collector.start_collecting()

# # Ici, insérez le code que vous souhaitez surveiller

# data_collector.stop_collecting()


