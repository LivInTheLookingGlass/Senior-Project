import optparse, settings

def main():
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
                      dest='propagate-factor',
                      default=None,
                      help='Minimum funds:reward ratio you'll propagate bounties at')
                      
    (options, args) = parser.parse_args()
    
if __name__ == "__main__":
    main()
