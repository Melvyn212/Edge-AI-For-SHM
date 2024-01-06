import subprocess
import json
import csv
import os
import subprocess


SHELLY_SCRIPT_PATH = './Shelly/shelly.py'

import csv

def json_to_csv(json_data, csv_file_name):
    # Assurez-vous que json_data est une liste de dictionnaires
    if not json_data or not isinstance(json_data, list):
        return

    # Modifier les valeurs de la colonne 'power' avant d'écrire
    for row in json_data:
        if 'power' in row:
            row['power'] = row['power'] * 1000

    # Écrire dans le fichier CSV
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)
        


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

def start_script(script_id,endpoint):
    output_a = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'start', str(script_id)])
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'call', str(script_id), endpoint])   
    print(output_a)

def call_script(logfile, csv_file_name):

    try:
      with open(logfile, 'r') as fichier:
         json_data = json.load(fichier)
    except json.JSONDecodeError:
        print("Erreur lors de la conversion des données JSON.")
        return None

    json_to_csv(json_data, csv_file_name)


def stop_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'stop', str(script_id)])
    print(output)

def delete_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'delete', str(script_id)])
    print(output)


def getdata(log_file_path):
    """ Exécute un script bash avec un chemin de fichier de log en paramètre et retourne l'objet processus. """
    default_script_path = 'Shelly/getdata.sh'

    # Assurez-vous que le chemin du fichier de log est fourni
    if not log_file_path:
        raise ValueError("Un chemin de fichier de log doit être fourni")

    # Démarrer le processus en arrière-plan
    process = subprocess.Popen(['bash', default_script_path, log_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def stop_process(process):
    """ Arrête le processus en cours d'exécution. """
    process.kill()  # Envoie un signal SIGTERM
    try:
        process.wait(timeout=5)  # Attend que le processus se termine, avec un timeout
    except subprocess.TimeoutExpired:
        process.kill()  # Force l'arrêt du processus si le SIGTERM ne fonctionne pas
    print("Processus arrêté.")

