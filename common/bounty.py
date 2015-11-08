import os, pickle
from common.safeprint import safeprint

bountyList = []

class Bounty:
  ip = ""
  btc = ""
  reward = 0
  data = []
  
  def __init__(ipAddress, btcAddress, rewardAmount):
    ip = ipAddress
    btc = btcAddress
    reward = rewardAmount
  
  def __init__(ipAddress, btcAddress, rewardAmount, dataList):
    ip = ipAddress
    btc = btcAddress
    reward = rewardAmount
    data = dataList
  
  def addData(dataList):
    data = dataList
    
  def isValid():
    #ping ip
    #check if all fields have things
    return False
  
  def isPayable():
    #check if address has enough
    return False

def saveToFile():
  if os.path.exists("bounties.pickle"):
    pickle.dump(boutyList,"bounties.pickle")
    return True
  return False

def loadFromFile():
  if os.path.exists("settings.conf"):
    bountyList = pickle.load("bounties.pickle")
    return True
  return False

def loadBounties():
  loadFromFile()
  if len(bountyList) is 0:
    requestBounties()
  return len(bountyList) is not 0

def requestBounties(peerList):
  for peer in peerList:
    bountyList.extend(requestBounty(peer))
    
def requestBounty(peer):
  safeprint("currently unsupported")

def sendBounty(peer):
  safeprint("currently unsupported")
  if len(bountyList) is 0:
    loadBounties()
  #send bounties
  dumpBounties()

def getBounty(charity, factor):
  for bounty in bountyList:
    if best is None:
      best = bounty
    elif best.rewardAmount < bounty.rewardAmount and bounty.isValid() and (isPayable(factor) or charity):
      best = bounty
  return best
