import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class DataPlotter:
    def __init__(self, data, sampling_rate):
        """
        Initialize the DataPlotter with data and a sampling rate.

        :param data: Can be a pandas.DataFrame or a numpy.ndarray.
        :param sampling_rate: float, the rate at which data was sampled per second.
        """
        self.data = data
        self.sampling_rate = sampling_rate

    def plot_series(self, series=None, percentage=100, title=None, xlabel='Time (s)', ylabel='Amplitude'):
        """
        Plot a percentage of a time series.

        :param series: Can be a string (name of the column in pandas.DataFrame) or an integer (index of the series in numpy.ndarray).
        :param percentage: float, percentage of the data to plot (0-100).
        :param title: string, the title of the plot.
        :param xlabel: string, the label for the x-axis.
        :param ylabel: string, the label for the y-axis.
        """
        if isinstance(self.data, pd.DataFrame):
            if not isinstance(series, str) or series not in self.data.columns:
                raise ValueError(f"Series '{series}' not found in the DataFrame.")
            data_to_plot = self.data[series]
        elif isinstance(self.data, np.ndarray):
            if not isinstance(series, int) or series < 0 or series >= self.data.shape[1]:
                raise ValueError(f"Series index {series} is out of bounds for the array with shape {self.data.shape}.")
            data_to_plot = self.data[:, series]
        else:
            raise TypeError("Data must be a pandas.DataFrame or a numpy.ndarray.")

        num_data_points = int(len(data_to_plot) * (percentage / 100))
        data_to_plot = data_to_plot[:num_data_points]
        time_axis = np.arange(num_data_points) / self.sampling_rate

        plt.figure(figsize=(12, 6))
        plt.plot(time_axis, data_to_plot, label='Time Series Signal')
        plt.title(title if title else 'Time Series Plot')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.legend()
        plt.show()

# Example usage with a numpy array:
# Assuming 'vibration_data' is your numpy array with multiple time series and 'fs' is the sampling rate.
# To plot 50% of the first time series (index 0) in the array:
# plotter = DataPlotter(vibration_data, fs)
# plotter.plot_series(series=0, percentage=50)
