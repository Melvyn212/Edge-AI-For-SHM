#!/bin/bash

# Variables globales pour les chemins
CPU_PATH="/sys/devices/system/cpu"
GPU_PATH="/sys/devices/57000000.gpu/devfreq/57000000.gpu"

# Vérifier si l'utilisateur a les droits sudo
if [ "$(id -u)" != "0" ]; then
    echo "Ce script doit être exécuté avec des privilèges root."
    exit 1
fi

# Fonction pour activer/désactiver un cœur CPU
set_cpu_state() {
    cpu_id=$1
    state=$2

    if [[ $cpu_id -lt 0 || $state -lt 0 || $state -gt 1 ]]; then
        echo "Paramètres invalides pour set_cpu_state."
        return 1
    fi

    echo $state > "${CPU_PATH}/cpu${cpu_id}/online"
    if [ $? -ne 0 ]; then
        echo "Impossible de modifier l'état du CPU $cpu_id."
        return 1
    fi
}

# Fonction pour régler la fréquence maximale du CPU en pourcentage du max
set_cpu_freq_percentage() {
    cpu_id=$1
    percentage=$2

    if [[ $cpu_id -lt 0 || $percentage -lt 0 || $percentage -gt 100 ]]; then
        echo "Paramètres invalides pour set_cpu_freq_percentage."
        return 1
    fi

    max_freq=$(cat "${CPU_PATH}/cpu${cpu_id}/cpufreq/cpuinfo_max_freq")
    min_freq=$(cat "${CPU_PATH}/cpu${cpu_id}/cpufreq/cpuinfo_min_freq")
    target_freq=$(( max_freq * percentage / 100 ))

    if [ $target_freq -lt $min_freq ]; then
        target_freq=$min_freq
    fi

    echo $target_freq > "${CPU_PATH}/cpu${cpu_id}/cpufreq/scaling_max_freq"
    if [ $? -ne 0 ]; then
        echo "Impossible de régler la fréquence du CPU $cpu_id."
        return 1
    fi
}

# Fonction pour régler la fréquence maximale du GPU en pourcentage du max
set_gpu_freq_percentage() {
    percentage=$1

    if [[ $percentage -lt 0 || $percentage -gt 100 ]]; then
        echo "Paramètres invalides pour set_gpu_freq_percentage."
        return 1
    fi

    max_freq=$(cat "${GPU_PATH}/max_freq")
    min_freq=$(cat "${GPU_PATH}/min_freq")
    target_freq=$(( max_freq * percentage / 100 ))

    if [ $target_freq -lt $min_freq ]; then
        target_freq=$min_freq
    fi

    echo $target_freq > "${GPU_PATH}/max_freq"
    if [ $? -ne 0 ]; then
        echo "Impossible de régler la fréquence du GPU."
        return 1
    fi
}

# Fonction pour maximiser les performances
maximize_performance() {
    /usr/bin/jetson_clocks
}

# Vérification des arguments et exécution des commandes
case "$1" in
    max)
        maximize_performance
        ;;
    min)
        for cpu in ${CPU_PATH}/cpu[0-3]*; do
            cpu_id=$(basename $cpu | cut -d 'u' -f 2)
            set_cpu_state $cpu_id 1
            min_freq=$(cat "${cpu}/cpufreq/cpuinfo_min_freq")
            echo $min_freq > "${cpu}/cpufreq/scaling_max_freq"
        done
        ;;
    *)
        if [ "$#" -eq 3 ]; then
            cpu_id=$1
            cpu_percentage=$2
            gpu_percentage=$3

            set_cpu_state $cpu_id 1
            set_cpu_freq_percentage $cpu_id $cpu_percentage
            set_gpu_freq_percentage $gpu_percentage
        else
            echo "Usage:"
            echo "$0 max - Maximiser les performances"
            echo "$0 min - Définir les fréquences au minimum"
            echo "$0 {cpu_id} {cpu_percentage} {gpu_percentage} - Définir les fréquences en pourcentage"
        fi
        ;;
esac
