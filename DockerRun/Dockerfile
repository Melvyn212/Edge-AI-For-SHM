# Image de base TensorFlow pour Jetson nano source : https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-tensorflow
FROM nvcr.io/nvidia/l4t-tensorflow:r32.4.4-tf1.15-py3

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

RUN pip3 install codecarbon

RUN pip3 install --upgrade matplotlib

RUN apt-get install -y git

RUN pip3 install git+https://github.com/thu-ml/zhusuan.git

RUN pip3 install git+https://github.com/haowen-xu/tfsnippet.git@v0.2.0-alpha1

RUN pip3 install imageio==2.4.1

RUN pip3 install fs==2.3.0
RUN pip3 install tqdm==4.28.1
RUN pip3 install click==7.0
RUN pip3 install six==1.11.0
RUN pip3 install tensorflow_probability==0.8
RUN pip3 install numpy

RUN apt-get install -y jq


# Installer scikit-learn et nettoyer
RUN apt-get install -y python3-sklearn && \
    rm -rf /var/lib/apt/lists/*

CMD ["python3","EdgeAI/main.py"]