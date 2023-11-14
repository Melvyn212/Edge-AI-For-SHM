import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import KernelPCA
from sklearn.mixture import GaussianMixture
import joblib
import warnings

class DataNormalization:
    def __init__(self, method='MSD', options=None):
        self.method = method
        self.options = options if options is not None else {}
        self.model = None
        self._validate_options()
        self._initialize_model()

    def _validate_options(self):
        valid_methods = ['MSD', 'GMM', 'KPCA', 'GKPCA']
        if self.method not in valid_methods:
            raise ValueError(f"Method must be one of {valid_methods}")
        if self.method in ['KPCA', 'GKPCA'] and 'n_components' not in self.options:
            raise ValueError("n_components option must be specified for KPCA and GKPCA methods")

    def _initialize_model(self):
        try:
            if self.method == 'MSD':
                self.model = StandardScaler()
            elif self.method == 'GMM':
                self.model = GaussianMixture(n_components=self.options.get('n_components', 1))
            elif self.method in ['KPCA', 'GKPCA']:
                kernel = 'rbf' if self.method == 'KPCA' else self.options.get('kernel', 'rbf')
                self.model = KernelPCA(n_components=self.options['n_components'], kernel=kernel)
        except Exception as e:
            raise e

    def fit(self, X):
        try:
            self.model.fit(X)
        except Exception as e:
            raise e

    def transform(self, X):
        try:
            if self.method == 'GMM':
                return self.model.predict_proba(X)
            else:
                return self.model.transform(X)
        except Exception as e:
            raise e

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def save_model(self, path):
        joblib.dump(self.model, path)

    def load_model(self, path):
        self.model = joblib.load(path)

    def reset(self):
        self._initialize_model()

# Usage Example:
# try:
#     data = loaded_data
#     normalized_data = DataNormalization(method='GMM').fit_transform(data)
#     normalizer.save_model('normalizer.pkl')
# except ValueError as ve:
#     print(ve)
# except Exception as e:
#     print("An error occurred:", e)
# print(normalized_data)