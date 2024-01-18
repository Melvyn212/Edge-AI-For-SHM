from codecarbon import EmissionsTracker
from tegrastats_parser.tegrastats import Tegrastats
from tegrastats_parser.parse import Parse
from tools import create_output_directory
from tools import plot
from tools import plot_loss

from Shelly.shellyData import create_script
from Shelly.shellyData import start_script
from Shelly.shellyData import call_script
from Shelly.shellyData import stop_script
from Shelly.shellyData import delete_script
from Shelly.shellyData import getdata
from Shelly.shellyData import stop_process
import time
import os
import subprocess

import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)



#base_path="/home/adehundeag/Edge-AI-For-SHM/Core"
base_path='/output'
output_path=create_output_directory(base_path)
# ########################################################################################
#Frequences processeurs
freqState="EdgeAI/cpu_gpu_setting/state.sh"
freqState_out=os.path.join(output_path, "GPU_CPU_Freq")

subprocess.run(['bash', freqState, freqState_out])

# ########################################################################################
#SHELLY

create_script('power', '/EdgeAI/Shelly/PowerTracker.js')
start_script(1,"api?yield")
shelly_log_file = os.path.join(output_path, 'log.json')
shelly_process = getdata(shelly_log_file) 
shelly_csv_file=os.path.join(output_path, 'shelly.csv')

# #########################################################################################
#Codecarbon
tracker = EmissionsTracker(output_dir=output_path,log_level="ERROR")
tracker.start()
# ########################################################################################

#tegrastats
interval = 1000 #ms
tegr_log_file = os.path.join(output_path, 'tegra_output_log.txt')
tegr_csv_file=os.path.join(output_path, 'tegra_output_log.csv')
verbose = False
tegrastats = Tegrastats(interval, tegr_log_file, verbose)
process,current_time=tegrastats.run()

# #CODE A MONITORER
# #########################################################################################

time.sleep(30)


def run_script(script_name, argument1=None, argument2=None, argument3=None,  argument4=None):
    # Construire la liste de commande
    command = ["python3", script_name]
    if argument1:
        command.append(argument1)
    if argument2:
        command.append(argument2)
    if argument3:
        command.append(argument3)
    if argument4:
        command.append(argument4)
    try:
        # Exécuter la commande
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # Afficher la sortie standard
        print(f"Sortie du script: {result.stdout}")

    except subprocess.CalledProcessError as e:
        # Afficher l'erreur en cas d'échec
        print(f"Erreur lors de l'exécution du script: {e.stderr}")


if __name__ == "__main__":
    processed=os.path.join(output_path, 'processed')
    result=os.path.join(output_path, 'result')
    training_log=os.path.join(result, 'training_log.csv')
    run_script("/EdgeAI/MODEL/OmniAnomaly/data_preprocess.py","MSL",processed)
    print(f"\nLes données ont bien été traitées\n")
    with tf.device('/GPU:0'):
        run_script("/EdgeAI/MODEL/OmniAnomaly/main.py",result,processed,training_log)

time.sleep(30)





# #########################################################################################
# #FIN DU CODE A MONITORER
# #########################################################################################

# #SHELLY

stop_process(shelly_process)
stop_script(1)
delete_script(1)
call_script(shelly_log_file,shelly_csv_file)

# ########################################################################################

#tegrastats
tegrastats.stop(process)
parser = Parse(interval, tegr_log_file,current_time)
parser.parse_file()
# ########################################################################################

#Codecarbon
emissions = tracker.stop()
print(f"Emissions: {emissions} kg")

# ########################################################################################



file_info_list = [
     (tegr_csv_file, 'Time (mS)', 'Current POM_5V_IN Power Consumption (mW)',"Tegrastats",1),
    (tegr_csv_file, 'Time (mS)', 'Average POM_5V_IN Power Consumption (mW)',"Tegrastats_AVG",1),
     (shelly_csv_file, 'timestamp', 'power',"Shelly",0)



        # Ajouter d'autres fichiers et colonnes selon le besoin et ne pas oublier le skiprows a la fin
]

file_info_list_1 = [
    (training_log, 'Step', 'Training Loss',"Loss",0)

        # Ajouter d'autres fichiers et colonnes selon le besoin et ne pas oublier le skiprows a la fin
]


output_file = os.path.join(output_path, 'power_consumption_plot.png')
output_file_1 = os.path.join(output_path, 'Loss.png')

plot(file_info_list, output_file)
plot_loss(file_info_list_1, output_file_1)



