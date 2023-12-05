import subprocess
import re


def get_tegrastat_data():
    try:
        output = subprocess.check_output(['tegrastat'], text=True)

        ram_usage = re.search(r'RAM (\d+)/(\d+)MB', output)
        swap_usage = re.search(r'SWAP (\d+)/(\d+)MB', output)
        cpu_usage = re.search(r'CPU \[(.*?)\]', output)
        gpu_temp = re.search(r'GPU@(\d+)C', output)
        cpu_temp = re.search(r'CPU@(\d+)C', output)

        data = {
            'ram_usage': ram_usage.group(1) if ram_usage else None,
            'ram_total': ram_usage.group(2) if ram_usage else None,
            'swap_usage': swap_usage.group(1) if swap_usage else None,
            'swap_total': swap_usage.group(2) if swap_usage else None,
            'cpu_usage': cpu_usage.group(1) if cpu_usage else None,
            'gpu_temp': gpu_temp.group(1) if gpu_temp else None,
            'cpu_temp': cpu_temp.group(1) if cpu_temp else None,
        }

        return data
