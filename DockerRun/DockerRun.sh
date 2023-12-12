#!/bin/bash
USER="jwu"
# Définissez les chemins dans des variables
TEGRASTATS_PATH="/usr/bin/tegrastats"
CODE_PATH="/home/${USER}/Edge-AI-For-SHM/Core"
OUTPUT_PATH="/home/${USER}Edge-AI-For-SHM/output"
DOCKER_IMAGE="melvyn212/edge_ai_jnano:latest"

# Exécutez le conteneur Docker avec les volumes montés
sudo docker run -it --rm \
-v "${TEGRASTATS_PATH}:${TEGRASTATS_PATH}:ro" \
-v "${CODE_PATH}:/EdgeAI:ro" \
-v "${OUTPUT_PATH}:/output" \
"${DOCKER_IMAGE}"

#./DockerRun.sh