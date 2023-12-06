import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.utils import to_categorical

class IrisModel:
    def __init__(self, num_features, num_classes):
        # Initialisation du modèle
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(num_features,)),
            Dense(64, activation='relu'),
            Dense(num_classes, activation='softmax')
        ])

        # Compilation du modèle
        self.model.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    def train(self, X_train, y_train, X_val, y_val, epochs=10):
        # Entraînement du modèle
        self.history = self.model.fit(X_train, y_train, epochs=epochs, validation_data=(X_val, y_val))

    def evaluate(self, X_test, y_test):
        # Évaluation du modèle
        return self.model.evaluate(X_test, y_test)

    def predict(self, X_new):
        # Prédiction sur de nouvelles données
        return self.model.predict(X_new)
