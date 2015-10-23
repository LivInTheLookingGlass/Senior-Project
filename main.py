from bounty import *
from peers import *
import settings

def main():
    settings.setup()
    print "settings are:"
    print settings.config
    
if __name__ == "__main__":
    main()
