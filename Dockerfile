FROM nvcr.io/nvidia/l4t-base:r32.4.4

RUN apt-get update && apt-get install -y --fix-missing \
    make \
    g++ \
    python3-pip \
    libopenblas-base \
    libopenmpi-dev \
    python3-h5py \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip

COPY requirements.txt 

# Installer les dépendances Python
RUN pip3 install -r requirements.txt

# Copier le reste des fichiers de l'application dans le répertoire de travail
COPY . /SHM
WORKDIR /SHM


# Définir une variable d'environnement pour que le modèle sache qu'il fonctionne dans un conteneur Docker
ENV RUNNING_IN_DOCKER=true

# Commande pour démarrer l'application
CMD ["python3", "main.py"]
