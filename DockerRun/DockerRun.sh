#!/bin/bash

# Définissez les chemins dans des variables
TEGRASTATS_PATH="/usr/bin/tegrastats"
CODE_PATH="/home/adehundeag/Edge-AI-For-SHM"
OUTPUT_PATH="/home/adehundeag/Edge-AI-For-SHM/output"
DOCKER_IMAGE="tensorflow_test3:latest"

# Exécutez le conteneur Docker avec les volumes montés
sudo docker run -it --rm \
-v "${TEGRASTATS_PATH}:${TEGRASTATS_PATH}:ro" \
-v "${CODE_PATH}:/data:ro" \
-v "${OUTPUT_PATH}:/output" \
"${DOCKER_IMAGE}"
