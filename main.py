from common.bounty import *
from common.peers import *
from common import settings
from time import sleep
from common.safeprint import safeprint

def main():
    settings.setup()
    try:
        import miniupnpc
    except:
        settings.config['outbound'] = True
    safeprint("settings are:")
    safeprint(settings.config)
    ear = listener(settings.config['port'],settings.config['outbound'])
    ear.daemon = True
    ear.start()
    sleep(5)
    initializePeerConnections(settings.config['port'])
    
if __name__ == "__main__":
    main()
