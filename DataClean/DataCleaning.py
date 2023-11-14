import numpy as np
from sklearn.impute import SimpleImputer
from scipy.signal import decimate
from scipy import stats

class DataCleaning:
    def __init__(self, data, imputation_strategy='mean', decimation_factor=2):
        """
        Initialize the DataCleaning class with the dataset and parameters for imputation and decimation.
        
        :param data: The dataset to clean, expected to be a numpy array or a similar structure.
        :param imputation_strategy: Strategy for imputation (e.g., 'mean', 'median', 'most_frequent', or 'constant').
        :param decimation_factor: The factor by which to downsample the data.
        """
        self.data = np.array(data)
        self.imputer = SimpleImputer(strategy=imputation_strategy)
        self.decimation_factor = decimation_factor

    def impute(self):
        """
        Impute missing values in the dataset using the specified strategy.
        """
        self.data = self.imputer.fit_transform(self.data)
        return self.data

    def decimate(self):
        """
        Decimate the data to downsample it by the specified factor.
        """
        self.data = np.apply_along_axis(lambda x: decimate(x, self.decimation_factor), axis=0, arr=self.data)
        return self.data

    def remove_outliers(self):
        """
        Remove outliers from the dataset using the IQR method.
        """
        Q1 = np.percentile(self.data, 25, axis=0)
        Q3 = np.percentile(self.data, 75, axis=0)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Create a mask for each feature column (False for values that are not outliers)
        mask = np.all((self.data >= lower_bound) & (self.data <= upper_bound), axis=1)
        self.data = self.data[mask]
        return self.data

    def run(self):
        """
        Execute the full data cleaning pipeline.
        """
        self.impute()
        self.remove_outliers()
        self.decimate()
        return self.data

# # Exemple d'utilisation
# raw_data = ...  # Votre jeu de données brut
# cleaner = DataCleaning(raw_data)
# cleaned_data = cleaner.run()
