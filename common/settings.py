import optparse, os, pickle
from common.safeprint import safeprint

config = {'charity':False,
          'propagate_factor':2,
          'accept_latency':2000,
          'server':False,
	  'port':44565}
settings_file = "data" + os.sep + "settings.conf"

def saveSettings():
    if not os.path.exists(settings_file.split(os.sep)[0]):
        os.mkdir(settings_file.split(os.sep)[0])
    pickle.dump(config,open(settings_file,"wb"),2)

def loadSettings():
    if os.path.exists(settings_file):
        config.update(pickle.load(open(settings_file,"rb")))

def setup():
    parser = optparse.OptionParser()
    parser.add_option('-c',
                      '--charity',
                      dest='charity',
                      default=None,
                      action="store_true",
                      help='Sets whether you accept rewardless bounties')
    parser.add_option('-l',
                      '--latency',
                      dest='accept_latency',
                      default=None,
                      help='Maximum acceptable latency from a server')
    parser.add_option('-f',
                      '--propagation-factor',
                      dest='propagate_factor',
                      default=None,
                      help='Minimum funds:reward ratio you\'ll propagate bounties at')
    parser.add_option('-S',
                      '--server',
                      dest='server',
                      default=None,
                      action="store_true",
                      help='Sets whether you operate as a server or client (Default: client)')        
    (options, args) = parser.parse_args()

    safeprint("options parsed")
    overrides = options.__dict__  
    loadSettings()
    saveSettings()
    kill = []
    for key in overrides:
        if overrides.get(key) is None:
            kill += [key]
    for key in kill:
        overrides.pop(key)
    config.update(overrides)
