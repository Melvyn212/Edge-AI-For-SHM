from DataAcquisition import DataAcquisition


def main():

    # Définir le chemin de stockage pour les données
    file_path = "C:\Users\USER\OneDrive\Bureau\github\vibro\0D.csv"

    loaded_data = DataAcquisition.load_data(file_path)

if __name__ == "__main__":
    main()
