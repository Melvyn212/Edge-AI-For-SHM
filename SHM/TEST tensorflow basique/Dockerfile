# Utiliser l'image de base TensorFlow pour Jetson
FROM nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf2.3-py3

# Mettre à jour et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt dans le conteneur
# COPY requirement.txt .

# Installer les paquets Python spécifiés dans requirements.txt
# RUN pip3 install --no-cache-dir -r requirement.txt

# Copier les fichiers de votre projet dans le conteneur (facultatif)
# COPY . /app
# WORKDIR /app

# Commande par défaut au démarrage du conteneur
# CMD ["python3", "script.py"]
