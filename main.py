from common.bounty import *
from common.peers import *
from common import settings
from time import sleep

def main():
    settings.setup()
    print "settings are:"
    print settings.config
    ear = listener(1,settings.config['port'])
    ear.daemon = True
    ear.start()
    initializePeerConnections()
    
if __name__ == "__main__":
    main()
