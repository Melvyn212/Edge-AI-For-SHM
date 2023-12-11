import subprocess
import json
import csv
import os

SHELLY_SCRIPT_PATH = './EdgeAI/Shelly/shelly.py'

import csv

def json_to_csv(json_data, csv_file_name):
    # Assurez-vous que json_data est une liste de dictionnaires
    if not json_data or not isinstance(json_data, list):
        return

    # Modifier les valeurs de la colonne 'power' avant d'écrire
    for row in json_data:
        row['power'] = row['power'] * 1000 if 'power' in row else row['power']

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)

# Exemple d'utilisation
json_data = [
    {"current": 0.023, "power": 1.7, "timestamp": 1702223808, "voltage": 225.7},
    {"current": 0.023, "power": 1.7, "timestamp": 1702223809, "voltage": 225.7}
]

json_to_csv(json_data, "output.csv")


import subprocess

def run_command(command):
    try:
        # Remplacer 'text=True' par 'universal_newlines=True'
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e.stderr}")
        return None



def create_script(script_name, script_file):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'create', script_file, script_name])
    print(output)

def start_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'start', str(script_id)])
    print(output)

def call_script(script_id, endpoint, csv_file_name, csv_file_path):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'call', str(script_id), endpoint])

    try:
        json_data = json.loads(output)
    except json.JSONDecodeError:
        print("Erreur lors de la conversion des données JSON.")
        return None

    # Construire le chemin complet du fichier CSV
    full_csv_file_path = os.path.join(csv_file_path, csv_file_name)
    
    json_to_csv(json_data, full_csv_file_path)
    return full_csv_file_path



def stop_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'stop', str(script_id)])
    print(output)

def delete_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'delete', str(script_id)])
    print(output)


# if __name__ == '__main__':
#     # Exemple d'utilisation
#     create_script('power', 'PowerTracker.js')
#     start_script(1)
#     csv_file = call_script(1, "api?yield", "mesure.csv",'/home/adehundeag/Edge-AI-For-SHM/Core/Shelly')
#     if csv_file:
#         print(f"Les données ont été enregistrées dans {csv_file}")
#     stop_script(1)
#     delete_script(1)
