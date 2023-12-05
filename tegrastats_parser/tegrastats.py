import subprocess

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
        try:
            process = subprocess.Popen(cmd, shell=True)
            print("Running tegrastats...")
            return process
        except subprocess.CalledProcessError:
            print(f"Error running tegrastats!\nCommand used {cmd}")
            return None

    def stop(self, process):
        if process is not None:
            try:
                process.terminate()
                process.wait()
                print("Successfully stopped tegrastats!")
            except subprocess.CalledProcessError:
                print(f"Unable to kill tegrastats (pid={process.pid}) successfully...")
                return False
        return True

