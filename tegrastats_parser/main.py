import argparse
from tegrastats import Tegrastats
from parse import Parse
import subprocess

def start_measuring(interval, log_file='output_log.txt'):
    cmd = f"tegrastats --interval {interval} > {log_file}"
    return subprocess.Popen(cmd, shell=True)

def stop_measuring(process):
    process.terminate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', action='store_true', help='Start measuring power consumption')
    parser.add_argument('--stop', action='store_true', help='Stop measuring power consumption')
    parser.add_argument('--interval', '-i', type=int, default=1000, help='Logging interval in milliseconds')
    parser.add_argument('--log_file', '-f', default='output_log.txt', help='Log file name for data')
    options = parser.parse_args()

    process = None

    if options.start:
        process = start_measuring(options.interval, options.log_file)

    if options.stop and process:
        stop_measuring(process)
        parser = Parse(options.interval, options.log_file)
        csv_file = parser.parse_file()

