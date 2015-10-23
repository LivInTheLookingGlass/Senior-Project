import os, pickle

seedlist = []
list = []

def getFromFile():
  if os.path.exists("peerlist.pickle"):
    list = pickle.load("peerlist.pickle")

def saveToFile():
  if os.path.exists("peerlist.pickle"):
    pickle.dump(list,"peerlist.pickle")

def getFromSeeds():
  for seed in seedlist:
    list = list + requestPeerlist(seed)

def requestPeerlist(address):
  print "currently unsupported"
  return []
  
def sendPeerlist(address):
  print "currently unsupported"
  #send list

def initializePeerConnections():
  getFromFile()
  getFromSeeds()
  if len(list) < 12:
    for peer in list:
      list = list + requestPeerlist(peer)
  saveToFile()
