import optparse, os, pickle

config = {'accept_latency':2000,
          'charity':False,
          'outbound':False,
          'port':44565,
          'propagate_factor':2,
          'server':False,
          'verbose':0}
settings_file = "data" + os.sep + "settings.conf"

def saveSettings():
    """Save settings to a file"""
    if not os.path.exists(settings_file.split(os.sep)[0]):
        os.mkdir(settings_file.split(os.sep)[0])
    pickle.dump(config,open(settings_file,"wb"),0)

def loadSettings():
    """Load settings from a file"""
    from common.safeprint import safeprint
    if os.path.exists(settings_file):
        try:
            config.update(pickle.load(open(settings_file,"rb")))
        except:
            safeprint("Could not load from file")

def setup():
    """Parses and stores the command line arguments given, and override default and saved settings"""
    from common.safeprint import safeprint
    parser = optparse.OptionParser()
    parser.add_option('-c',
                      '--charity',
                      dest='charity',
                      default=None,
                      action="store_true",
                      help='Sets whether you accept rewardless bounties')
    parser.add_option('-f',
                      '--propagation-factor',
                      dest='propagate_factor',
                      default=None,
                      type="int",
                      help='Minimum funds:reward ratio you\'ll propagate bounties at')
    parser.add_option('-l',
                      '--latency',
                      dest='accept_latency',
                      default=None,
                      type="int",
                      help='Maximum acceptable latency from a server')
    parser.add_option('-o',
                      '--outbound-only',
                      dest='outbound',
                      default=None,
                      action="store_false",
                      help='Maximum acceptable latency from a server')
    parser.add_option('-p',
                      '--listening-port',
                      dest='port',
                      default=None,
                      type="int",
                      help='Port for the program to listen at')
    parser.add_option('-S',
                      '--server',
                      dest='server',
                      default=None,
                      action="store_true",
                      help='Sets whether you operate as a server or client (Default: client)')
    parser.add_option('-v',
                      dest='verbose',
                      default=None,
                      action="count",
                      help='Increments the level of verbosity (up to 3, default 1)')
    (options, args) = parser.parse_args()

    safeprint("options parsed")
    overrides = options.__dict__
    loadSettings()
    saveSettings()
    kill = []
    for key in overrides:               #Remove keys with None, just to be safe
        if overrides.get(key) is None:
            kill += [key]
    for key in kill:
        overrides.pop(key)
    config.update(overrides)
