#!/bin/bash

# Fonctions pour obtenir l'état et la fréquence du CPU et du GPU
get_cpu_state() {
    cpu_id=$1
    state=$(cat /sys/devices/system/cpu/cpu$cpu_id/online)
    echo "CPU $cpu_id: $([ $state -eq 1 ] && echo 'Actif' || echo 'Inactif')"
}

get_cpu_freq() {
    cpu_id=$1
    freq=$(cat /sys/devices/system/cpu/cpu$cpu_id/cpufreq/scaling_cur_freq)
    echo "Fréquence CPU $cpu_id: $freq Hz"
}

get_gpu_freq() {
    freq=$(cat /sys/devices/57000000.gpu/devfreq/57000000.gpu/cur_freq)
    echo "Fréquence GPU: $freq Hz"
}

# Vérifie si un chemin de fichier est fourni comme argument
output_file="$1"

# Fonction pour écrire les données
write_data() {
    for cpu_id in 0 1 2 3; do
        get_cpu_state $cpu_id
        get_cpu_freq $cpu_id
    done

    get_gpu_freq
}

# Écriture des données dans un fichier ou affichage sur la console
if [ -n "$output_file" ]; then
    write_data > "$output_file"
else
    write_data
fi
