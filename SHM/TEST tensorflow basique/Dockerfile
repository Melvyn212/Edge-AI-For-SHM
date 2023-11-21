# Utiliser l'image de base TensorFlow pour Jetson nano 
FROM nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf2.3-py3

RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install codecarbon

# COPY requirement.txt .
# RUN pip3 install --no-cache-dir -r requirement.txt

# COPY . /app
# WORKDIR /app

