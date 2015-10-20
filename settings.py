import os, pickle

def setup(overrides):
  config = []
  if os.path.exists("settings.conf"):
    config = pickle.load("settings.conf")
  else:
    config = ['charity':'false',
              'propagate_factor':'2',
              'accept_latency':'2000']
    pickle.dump(config,"settings.conf")
  config.update(overides)
