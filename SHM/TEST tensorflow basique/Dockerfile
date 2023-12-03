# Image de base TensorFlow pour Jetson nano source : https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-tensorflow
FROM nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf2.3-py3

# Mise à jour et mise à niveau des paquets
RUN apt-get update && apt-get upgrade -y

# Installation des locales et configuration de la locale UTF-8
RUN apt-get install -y locales && \
    locale-gen en_US.UTF-8

# Définir les variables d'environnement pour la locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Définir PYTHONIOENCODING à utf-8
ENV PYTHONIOENCODING=utf-8

# Installer scikit-learn et nettoyer
RUN apt-get install -y python3-sklearn && \
    rm -rf /var/lib/apt/lists/*

# Instructions supplémentaires pour votre Dockerfile...
