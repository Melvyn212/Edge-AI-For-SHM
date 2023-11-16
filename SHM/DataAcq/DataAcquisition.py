import os
import json
import datetime
import pandas as pd
import time
import threading

class DataAcquisition:
    def __init__(self, sensors, storage_path):
        """
        Initialize the DataAcquisition system with a set of sensors and a storage path.

        :param sensors: A list of sensor objects.
        :param storage_path: Path to the directory where the data will be stored.
        """
        self.sensors = sensors
        self.storage_path = storage_path
        self.stop_acquisition = False

    def collect_data(self):
        """
        Collect data from the defined sensors.

        :return: A list of data collected from sensors.
        """
        data = []
        for sensor in self.sensors:
            sensor_data = sensor.collect()  # Assuming each sensor has a collect method
            if sensor_data:
                data.append(sensor_data)
        return data

    def save_data(self, data):
        """
        Save the collected data to a file in JSON format.

        :param data: The data to be saved.
        :return: The file path where the data is saved.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"data_{timestamp}.json"
        file_path = os.path.join(self.storage_path, file_name)

        with open(file_path, 'w') as file:
            json.dump(data, file)

        return file_path

    @staticmethod
    def load_data(file_path):
        """
        Load the saved data from a local file into a pandas DataFrame.

        :param file_path: Path to the file containing the saved data.
        :return: A pandas DataFrame containing the loaded data.
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def collect_and_save(self):
        """
        Collect data from sensors and save it.

        :return: Path to the saved data file.
        """
        data = self.collect_data()
        file_path = self.save_data(data)
        return file_path

    def start_real_time_acquisition(self, interval=1):
        """
        Start real-time data acquisition from sensors.

        :param interval: Time interval (in seconds) between data acquisitions.
        """
        self.stop_acquisition = False
        self.acquisition_thread = threading.Thread(target=self._real_time_acquisition_loop, args=(interval,))
        self.acquisition_thread.start()

    def _real_time_acquisition_loop(self, interval):
        """
        Internal loop for real-time data acquisition.

        :param interval: Time interval between data acquisitions.
        """
        while not self.stop_acquisition:
            data = self.collect_data()
            if data:
                # Process or save the data here
                print("Data collected:", data)  # Example of displaying the data

            time.sleep(interval)

    def stop_real_time_acquisition(self):
        """
        Stop the real-time data acquisition.
        """
        self.stop_acquisition = True
        self.acquisition_thread.join()

# Example usage
# sensors = [Sensor1(), Sensor2(), ...]
# storage_path = "path/to/storage"
# data_acquisition = DataAcquisition(sensors, storage_path)
# data_acquisition.start_real_time_acquisition(interval=5)  # Collect data every 5 seconds
# data_acquisition.stop_real_time_acquisition()
