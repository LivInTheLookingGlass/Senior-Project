import multiprocessing, sys
from datetime import datetime
from common import settings

print_lock = multiprocessing.RLock()
silent_flag = multiprocessing.Value('b',False)


def safeprint(msg, verbosity=0):
    """Prints in a thread-lock, taking a single object as an argument"""
    if not silent_flag:
        string = ("[" + str(multiprocessing.current_process().pid) + "] " +
                  datetime.now().strftime('%H:%M:%S: ') + str(msg) + '\r\n')
        with print_lock:
            with open("output.txt", "a") as log:
                log.write(string)
            if settings.config.get('verbose') >= verbosity:
                sys.stdout.write(string)
