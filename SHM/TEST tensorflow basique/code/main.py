from codecarbon import EmissionsTracker

tracker = EmissionsTracker()
tracker.start()


from sklearn import datasets
from Processing import IrisDataProcessor  # Remplacez par le nom de votre fichier
from model import IrisModel  # Remplacez par le nom de votre fichier



def main():
    # Chargement de l'ensemble de données Iris
    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    # Initialisation et traitement des données
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


tracker.stop()