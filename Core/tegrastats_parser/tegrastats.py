import subprocess
import psutil
import os
import signal
import datetime


class Tegrastats:
    def __init__(self, interval, log_file, verbose):
        self.interval = interval
        self.log_file = log_file
        self.verbose = verbose

    def prepare_command(self):
        tegrastats_cmd = f"tegrastats --interval {self.interval}"

        if self.verbose:
            tegrastats_cmd = tegrastats_cmd + " --verbose"

        cmd = f"{{ echo $(date -u) & {tegrastats_cmd}; }} > {self.log_file}"
        return cmd

    def run(self):
        cmd = self.prepare_command()
        process = None

        try:
            process = subprocess.Popen(cmd,preexec_fn=os.setsid, shell=True)
            current_time_utc = datetime.datetime.utcnow().replace(microsecond=0)
            print("Running tegrastats...")
            return process,current_time_utc
        except subprocess.CalledProcessError:
            print(f"Error running tegrastats!\nCommand used {cmd}")
            return False
    
    
    def stop(self,process):
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print("Successfully stopped tegrastats!")
            return True
        except subprocess.CalledProcessError:
            print(f"Unable to kill tegrastats (pid={process.pid}) successfully...")
            return False

        