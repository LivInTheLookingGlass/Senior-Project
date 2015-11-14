import os, pickle, re
from common.safeprint import safeprint

bountyList = []

class Bounty:
  ip = ""
  btc = ""
  reward = 0
  data = []
  
  def __init__(self, ipAddress, btcAddress, rewardAmount, dataList=[]):
    self.ip = ipAddress
    self.btc = btcAddress
    self.reward = rewardAmount
    self.data = dataList
    
  def isValid(self):
    try:
      safeprint("Testing IP address")
      #is IP valid
      b = int(self.ip.split(":")[1]) in range(1024,49152)
      b = int(self.ip.split(":")[0].split(".")[0]) in range(0,256) and b
      b = int(self.ip.split(":")[0].split(".")[1]) in range(0,256) and b
      b = int(self.ip.split(":")[0].split(".")[2]) in range(0,256) and b
      b = int(self.ip.split(":")[0].split(".")[3]) in range(0,256) and b
      if not b:
        return False
      #ping IP
      #is Bitcoin address valid
      safeprint("Testing Bitcoin address")
      address = str(self.btc)
      #The following is a soft check
      #A deeper check will need to be done in order to assure this is correct
      if not re.match(re.compile("^[a-zA-Z1-9]{27,35}$"),address):
        return False
      #is reward valid
      safeprint("Testing reward")
      b = int(self.reward)
      return (b >= 0)
    except:
      return False
  
  def isPayable(self):
    #check if address has enough
    return False

def verify(string):
  test = pickle.loads(string)
  try:
    safeprint("Testing IP address")
    #is IP valid
    b = int(ip.split(":")[1]) in range(1024,49152)
    b = int(ip.split(":")[0].split(".")[0]) in range(0,256) and b
    b = int(ip.split(":")[0].split(".")[1]) in range(0,256) and b
    b = int(ip.split(":")[0].split(".")[2]) in range(0,256) and b
    b = int(ip.split(":")[0].split(".")[3]) in range(0,256) and b
    #ping IP
    #is Bitcoin address valid
    safeprint("Testing Bitcoin address")
    address = str(self.btc)
    #The following is a soft check
    #A deeper check will need to be done in order to assure this is correct
    if not re.match(re.compile("^[a-zA-Z1-9]{27,35}$"),address):
      return False
    #is reward valid
    safeprint("Testing reward")
    b = int(self.reward)
    return (b >= 0)
  except:
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
