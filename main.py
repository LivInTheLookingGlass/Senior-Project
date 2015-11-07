from common.bounty import *
from common.peers import *
from common import settings
from time import sleep
from common.safeprint import safeprint

def main():
    settings.setup()
    safeprint("settings are:")
    safeprint(settings.config)
    ear = listener(1,settings.config['port'])
    ear.daemon = True
    ear.start()
    initializePeerConnections()
    
if __name__ == "__main__":
    main()
