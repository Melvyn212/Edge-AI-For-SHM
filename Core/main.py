# from codecarbon import EmissionsTracker
from tegrastats_parser.tegrastats import Tegrastats
from tegrastats_parser.parse import Parse
from tools import create_output_directory
from tools import plot
from Shelly.shellyData import create_script
from Shelly.shellyData import start_script
from Shelly.shellyData import call_script
from Shelly.shellyData import stop_script
from Shelly.shellyData import delete_script
from Shelly.shellyData import getdata
from Shelly.shellyData import stop_process
import time
import os






#base_path="/home/adehundeag/Edge-AI-For-SHM/Core"
base_path='/output'
output_path=create_output_directory(base_path)

# ########################################################################################
#SHELLY

create_script('power', '/home/adehundeag/Edge-AI-For-SHM/Core/Shelly/PowerTracker.js')
start_script(1,"api?yield")
shelly_log_file = os.path.join(output_path, 'log.json')
shelly_process = getdata(shelly_log_file) 
shelly_csv_file=os.path.join(output_path, 'shelly.csv')

# #########################################################################################
# #Codecarbon
# tracker = EmissionsTracker(output_dir=output_path)
# tracker.start()
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

# from sklearn import datasets
# from Processing import IrisDataProcessor 
# from model import IrisModel 
# import time 

time.sleep(3600)



# def main():
#     # Chargement de l'ensemble de données Iris
#     iris = datasets.load_iris()
#     X, y = iris.data, iris.target

#     data_processor = IrisDataProcessor(X, y)
#     data_processor.split_data()
#     data_processor.normalize_features()
#     data_processor.encode_labels()
#     X_train, X_test, y_train_encoded, y_test_encoded = data_processor.get_processed_data()

#     # Initialisation du modèle
#     num_features = X_train.shape[1]
#     num_classes = data_processor.num_classes
#     model = IrisModel(num_features, num_classes)

#     # Entraînement du modèle
#     model.train(X_train, y_train_encoded, X_test, y_test_encoded, epochs=10)

#     # Évaluation du modèle
#     loss, accuracy = model.evaluate(X_test, y_test_encoded)
#     print(f"Test Accuracy: {accuracy*100:.2f}%")

# if __name__ == "__main__":
#     main()


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

# #Codecarbon
# emissions = tracker.stop()
# print(f"Emissions: {emissions} kg")

# ########################################################################################


file_info_list = [
    (tegr_csv_file, 'Time (mS)', 'Average POM_5V_IN Power Consumption (mW)',"Tegrastats",1),
     (shelly_csv_file, 'timestamp', 'power',"Shelly",0)
        # Ajouter d'autres fichiers et colonnes selon le besoin et ne pas oublier le skiprows a la fin
]
output_file = os.path.join(output_path, 'power_consumption_plot.png')

plot(file_info_list, output_file)


