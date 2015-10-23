import os, pickle

seedlist = []
peerlist = []

def getFromFile():
  if os.path.exists("peerlist.pickle"):
    peerlist = pickle.load("peerlist.pickle")

def saveToFile():
  if os.path.exists("peerlist.pickle"):
    pickle.dump(peerlist,"peerlist.pickle")

def getFromSeeds():
  for seed in seedlist:
    peerlist.extend(requestPeerlist(seed))

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
      peerlist.extend(requestPeerlist(peer))
  saveToFile()
