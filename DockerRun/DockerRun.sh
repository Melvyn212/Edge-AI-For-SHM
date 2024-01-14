#!/bin/bash
USER="adehundeag"

# Définissez les chemins dans des variables
TEGRASTATS_PATH="/usr/bin/tegrastats"
CODE_PATH="/home/${USER}/Edge-AI-For-SHM/Core"
OUTPUT_PATH="/home/${USER}/Edge-AI-For-SHM/output"
DOCKER_IMAGE="melvyn212/edge_ai_jnano:latest"

# Chemin vers les bibliothèques CUDA sur l'hôte
CUDA_LIB_PATH="/usr/local/cuda/lib64"

# Exécutez le conteneur Docker avec les volumes montés et le support CUDA
sudo docker run -it --rm --runtime nvidia \
-v "${TEGRASTATS_PATH}:${TEGRASTATS_PATH}:ro" \
-v "${CODE_PATH}:/EdgeAI" \
-v "${OUTPUT_PATH}:/output" \
-v "${CUDA_LIB_PATH}:${CUDA_LIB_PATH}:ro" \
-e LD_LIBRARY_PATH="${CUDA_LIB_PATH}:$LD_LIBRARY_PATH" \
"${DOCKER_IMAGE}"
