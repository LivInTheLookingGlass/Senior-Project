import multiprocessing, sys
from datetime import datetime
from common import settings

print_lock = multiprocessing.RLock()
max_digits = 0

def safeprint(msg, verbosity=0):
    """Prints in a thread-lock, taking a single object as an argument"""
    pid = str(multiprocessing.current_process().pid)
    max_digits = max(max_digits, len(pid))
    pid = pid.zfill(max_digits)
    string = ("[" + pid + "] " + datetime.now().strftime('%H:%M:%S: ') +
              str(msg) + '\n')
    with print_lock:
        with open("output.txt", "a") as log:
            log.write(string)
        if settings.config.get('verbose') >= verbosity:
            sys.stdout.write(string)
