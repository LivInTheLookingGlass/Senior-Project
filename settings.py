import os, pickle

defaults = {'charity':False,
            'propagate_factor':2,
            'accept_latency':2000}

def setup(overrides):
  config = {}
  if os.path.exists("settings.conf"):
    config = pickle.load("settings.conf")
  else:
    config = defaults
    pickle.dump(config,"settings.conf")
  for key in overrides:
    if overrides.get(key) is None:
      overrides.pop(key)
  config.update(overrides)
