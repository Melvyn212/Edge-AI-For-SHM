from tegrastats import Tegrastats
from parse import Parse
import time


interval = 1000
log_file = 'output_log.txt'
verbose = False

tegrastats = Tegrastats(interval, log_file, verbose)
process=tegrastats.run()

time.sleep(4)
tegrastats.stop(process)

parser = Parse(interval, log_file)
parser.parse_file()
