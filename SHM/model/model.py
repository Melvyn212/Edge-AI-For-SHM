import tensorflow as tf
from keras.backend import floatx, categorical_crossentropy
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Input, BatchNormalization, Dropout, Activation
from keras.models import load_model, Model
from keras.optimizers import Adam
from keras.regularizers import l1_l2
from sklearn.model_selection import train_test_split
from tensorflow import convert_to_tensor
from tensorflow.python.framework.smart_cond import smart_cond
from tensorflow.python.ops import math_ops, array_ops
from tensorflow.keras.utils import to_categorical

class CNNClassifier:
    def __init__(self, input_shape, num_classes, n_conv_layers=5, filter_size=9, n_dense_units=128, learning_rate=0.0001):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.n_conv_layers = n_conv_layers
        self.filter_size = filter_size
        self.n_dense_units = n_dense_units
        self.learning_rate = learning_rate
        self.model = self._build_model()

    def _build_model(self):
        inputs = Input(shape=(None,self.input_shape))
        x = inputs
        for i in range(self.n_conv_layers):
            x = Conv1D(filters=(i + 1) * 10, kernel_size=self.filter_size, padding="same", activation='relu')(x)
            x = BatchNormalization()(x)
            x = MaxPooling1D(pool_size=5, strides=2, padding="same")(x)
        x = Flatten()(x)
        x = Dense(units=self.n_dense_units, activation='relu')(x)
        x = Dropout(rate=0.5)(x)
        outputs = Dense(units=self.num_classes, activation='softmax')(x)

        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=Adam(lr=self.learning_rate), loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, X_train, y_train, X_val, y_val, batch_size=16, n_epochs=150, model_filepath='model.h5'):
        y_train = to_categorical(y_train, num_classes=self.num_classes)
        y_val = to_categorical(y_val, num_classes=self.num_classes)

        checkpoint = ModelCheckpoint(model_filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
        self.model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=n_epochs, batch_size=batch_size, callbacks=[checkpoint])

    def evaluate(self, X_test, y_test):
        y_test = to_categorical(y_test, num_classes=self.num_classes)
        return self.model.evaluate(X_test, y_test, verbose=0)

    def load(self, model_filepath):
        self.model = load_model(model_filepath)

# # Usage Example:
# if __name__ == '__main__':
#     # Assuming the data is loaded and preprocessed correctly.
#     X, y = load_data()  # Replace with actual data loading code
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     input_shape = X_train.shape[1:]
#     num_classes = np.unique(y).shape[0]

#     classifier = CNNClassifier(input_shape=input_shape, num_classes=num_classes)
#     classifier.train(X_train, y_train, X_test, y_test)
#     score = classifier.evaluate(X_test, y_test)
#     print(f'Test loss: {score[0]}')
#     print(f'Test accuracy: {score[1]}')

#     # Saving and loading the model
#     model_filepath = 'best_model.h5'
#     classifier.train(X_train, y_train, X_test, y_test, model_filepath=model_filepath)
#     classifier.load(model_filepath)
#     # Further evaluation or inference can be done here.

