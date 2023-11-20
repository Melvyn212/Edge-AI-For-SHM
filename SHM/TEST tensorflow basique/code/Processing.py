from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.utils import to_categorical
import numpy as np

class IrisDataProcessor:
    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.num_classes = len(np.unique(target))
        self.X_train, self.X_test, self.y_train, self.y_test = [None] * 4
        self.y_train_encoded, self.y_test_encoded = [None] * 2

    def split_data(self, test_size=0.2, random_state=42):
        # Division des données en ensembles d'entraînement et de test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.data, self.target, test_size=test_size, random_state=random_state)

    def normalize_features(self):
        # Normalisation des caractéristiques
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

    def encode_labels(self):
        # Encodage des étiquettes pour la classification
        self.y_train_encoded = to_categorical(self.y_train, self.num_classes)
        self.y_test_encoded = to_categorical(self.y_test, self.num_classes)

    def get_processed_data(self):
        # Retourne les données traitées
        return self.X_train, self.X_test, self.y_train_encoded, self.y_test_encoded
