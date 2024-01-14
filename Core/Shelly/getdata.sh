#!/bin/bash

finish() {
    # Ne fait rien à l'interruption, juste sortir du script
    exit
}

handle_error() {
    echo "Erreur lors de l'exécution de la commande. Arrêt du script."
    finish
}

trap finish SIGINT SIGTERM
trap handle_error ERR

logfile="${1:-/EdgeAI/Shelly/log.json}"

if [ ! "$logfile" ]; then
    echo "Usage: $0 path_to_log_file"
    exit 1
fi

# Initialiser le fichier avec un tableau vide []
echo '[]' > "$logfile"

while true; do
    output=$(./EdgeAI/Shelly/shelly.py -p scripts call 1 "api?yield" | jq '.[-1]')
    if [ ! -z "$output" ]; then
        # Utiliser jq pour ajouter les nouvelles données au tableau dans le fichier JSON
        jq --argjson new_data "$output" '. += [$new_data]' "$logfile" > temp.json && mv temp.json "$logfile"
    fi
    sleep 1
done