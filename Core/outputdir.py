import os
import datetime


def create_output_directory(base_path):
    # Obtenir l'heure actuelle
    current_time = datetime.datetime.now()
    # Formater l'heure pour l'inclure dans le nom du dossier (par exemple, 'output_2023_12_08_15_30_00')
    time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    directory_name = f"output_{time_str}"
    full_path = os.path.join(base_path, directory_name)

    os.makedirs(full_path)
    
    return full_path







