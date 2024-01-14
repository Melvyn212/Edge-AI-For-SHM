import subprocess
import json
import csv
import logging

SHELLY_SCRIPT_PATH = './EdgeAI/Shelly/shelly.py'
DEFAULT_SCRIPT_PATH = 'EdgeAI/Shelly/getdata.sh'

logging.basicConfig(level=logging.INFO)


def json_to_csv(json_data, csv_file_name):
    if not json_data or not isinstance(json_data, list):
        logging.error("Invalid json_data provided.")
        return

    for row in json_data:
        if 'power' in row:
            row['power'] = row['power'] * 1000

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)


def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command execution failed: {e.stderr}")
        return None


def create_script(script_name, script_file):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'create', script_file, script_name])
    logging.info(output)


def start_script(script_id, endpoint):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'start', str(script_id)])
    logging.info(output)
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'call', str(script_id), endpoint])
    logging.info(output)


def call_script(logfile, csv_file_name):
    try:
        with open(logfile, 'r') as file:
            json_data = json.load(file)
    except json.JSONDecodeError:
        logging.error("JSON decoding error.")
        return None

    json_to_csv(json_data, csv_file_name)


def stop_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'stop', str(script_id)])
    logging.info(output)


def delete_script(script_id):
    output = run_command([SHELLY_SCRIPT_PATH, '-p', 'scripts', 'delete', str(script_id)])
    logging.info(output)


def getdata(log_file_path):
    if not log_file_path:
        raise ValueError("Log file path must be provided")

    process = subprocess.Popen(['bash', DEFAULT_SCRIPT_PATH, log_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def stop_process(process):
    process.kill()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    logging.info("Process stopped.")