import os
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def create_output_directory(base_path):
    # Obtenir l'heure actuelle
    current_time = datetime.datetime.now()
    # Formater l'heure pour l'inclure dans le nom du dossier (par exemple, 'output_2023_12_08_15_30_00')
    time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    directory_name = f"output_{time_str}"
    full_path = os.path.join(base_path, directory_name)

    os.makedirs(full_path)
    os.chmod(full_path,0o777)
    
    return full_path


def plot(file_info_list, output_file):
    """
    Lit plusieurs fichiers CSV, trace les courbes de consommation de puissance en fonction du temps pour chaque fichier,
    et sauvegarde le graphique dans un fichier.

    Args:
    file_info_list (list of tuples): Liste contenant des tuples. Chaque tuple doit contenir 
                                     (file_path, time_column, power_column, label).
    output_file (str): Chemin du fichier où le graphique sera sauvegardé.

    Returns:
    None: Le graphique est sauvegardé dans un fichier.
    """

    plt.figure(figsize=(12, 6))

    for file_info in file_info_list:
        file_path, time_column, power_column, label, skiprows = file_info
        data = pd.read_csv(file_path, skiprows=skiprows)
        data[time_column] = pd.to_datetime(data[time_column], unit='s')
        plt.plot(data[time_column], data[power_column], label=label)

    plt.title("Comparaison de la consommation de puissance  ||  " + str(datetime.datetime.utcnow().strftime("%Y_%m_%d")+' UTC'))
    plt.xlabel("Temps")
    plt.ylabel("Consommation de puissance (mW)")
    plt.legend()
    plt.grid(True)

    plt.savefig(output_file)
    plt.close()

def plot_loss(file_info_list, output_file):

    plt.figure(figsize=(12, 6))

    for file_info in file_info_list:
        file_path, Steps, loss, label, skiprows = file_info
        data = pd.read_csv(file_path, skiprows=skiprows)
        plt.plot(data[Steps], data[loss], label=label)

    plt.title("Courbe de loss  ||  " + str(datetime.datetime.utcnow().strftime("%Y_%m_%d")+' UTC'))
    plt.xlabel("Steps")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    plt.savefig(output_file)
    plt.close()

    # Exemple d'utilisation
    # file_info_list = [
    #     ('output_log.csv', 'Time (mS)', 'Average POM_5V_IN Power Consumption (mW)',"o"),
    #     ('utput_log.csv', 'Time (mS)', 'Average POM_5V_IN Power Consumption (mW)',"u")
    #     # Ajouter d'autres fichiers et colonnes selon le besoin
    # ]
    # output_file = 'multiple_power_consumption_plot.png'

    # plot_multiple_power_consumptions_from_files(file_info_list, output_file)

    # # Retourner le chemin du fichier de sortie pour confirmation




file_info_list = [
    ("tegra_output_log.csv", 'Time (mS)', 'Current POM_5V_IN Power Consumption (mW)',"Tegrastats",1),
     ("shelly.csv", 'timestamp', 'power',"Shelly",0),    
         ("tegra_output_log.csv", 'Time (mS)', 'Average POM_5V_IN Power Consumption (mW)',"Tegrastats_AVG",1)


        # Ajouter d'autres fichiers et colonnes selon le besoin et ne pas oublier le skiprows a la fin
]

file_info_list_1 = [
    ("result/training_log.csv", 'Step', 'Training Loss',"Loss",0),

        # Ajouter d'autres fichiers et colonnes selon le besoin et ne pas oublier le skiprows a la fin
]

plot(file_info_list, 'power_consumption_plot.png')

plot_loss(file_info_list_1, 'Loss.png')


