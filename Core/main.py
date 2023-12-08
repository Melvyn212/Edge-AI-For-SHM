from codecarbon import EmissionsTracker
from tegrastats_parser.tegrastats import Tegrastats
from tegrastats_parser.parse import Parse
from outputdir import create_output_directory
import os

base_path='/output'
output_path=create_output_directory(base_path)

interval = 1000 #ms
log_file = os.path.join(output_path, 'output_log.txt')
verbose = False

tracker = EmissionsTracker(output_dir=output_path)
tracker.start()

tegrastats = Tegrastats(interval, log_file, verbose)
process=tegrastats.run()



#########################################################################################
#CODE A MONITORER
#########################################################################################

from sklearn import datasets
from Processing import IrisDataProcessor 
from model import IrisModel 
import time 

time.sleep(300)


def main():
    # Chargement de l'ensemble de données Iris
    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    data_processor = IrisDataProcessor(X, y)
    data_processor.split_data()
    data_processor.normalize_features()
    data_processor.encode_labels()
    X_train, X_test, y_train_encoded, y_test_encoded = data_processor.get_processed_data()

    # Initialisation du modèle
    num_features = X_train.shape[1]
    num_classes = data_processor.num_classes
    model = IrisModel(num_features, num_classes)

    # Entraînement du modèle
    model.train(X_train, y_train_encoded, X_test, y_test_encoded, epochs=10)

    # Évaluation du modèle
    loss, accuracy = model.evaluate(X_test, y_test_encoded)
    print(f"Test Accuracy: {accuracy*100:.2f}%")

if __name__ == "__main__":
    main()





#########################################################################################
#FIN DU CODE A MONITORER
#########################################################################################




tegrastats.stop(process)
parser = Parse(interval, log_file)
parser.parse_file()

emissions = tracker.stop()
print(f"Emissions: {emissions} kg")