from common import bounty

"""Contains overrides to the common.bounty package to deal with server-specific functions"""

def verify(string):
    test = pickle.loads(string)
    try:
        safeprint("Testing IP address")
        #is IP valid
        b = int(test.ip.split(":")[1]) in range(1024,49152)
        b = int(test.ip.split(":")[0].split(".")[0]) in range(0,256) and b
        b = int(test.ip.split(":")[0].split(".")[1]) in range(0,256) and b
        b = int(test.ip.split(":")[0].split(".")[2]) in range(0,256) and b
        b = int(test.ip.split(":")[0].split(".")[3]) in range(0,256) and b
        if not b:
            return False
        #ping IP
        #is Bitcoin address valid
        safeprint("Testing Bitcoin address")
        address = str(test.btc)
        #The following is a soft check
        #A deeper check will need to be done in order to assure this is correct
        if not checkAddressValid(address):
            return False
        #is reward valid
        safeprint("Testing reward")
        b = int(test.reward)
        return (b >= 0)
    except:
        return False

def addBounty(bounty):
    a = False
    safeprint((sys.version_info[0],sys.version_info[1],sys.version_info[2]))
    if sys.version_info[0] == 2 and sys.version_info[1] == 6 and (type(bounty) == type("aaa") or type(bounty) == type(unicode("aaa"))):
        safeprint("Fed as string in 2.6; encoding ascii and ignoring errors")
        try:
            bounty = bounty.encode('ascii','ignore')
        except:
            bounty = str(bounty)
    elif type(bounty) == type("aaa") and sys.version_info[0] >= 3:
        safeprint("Fed as string; encoding utf-8")
        bounty = bounty.encode('utf-8')
    safeprint("External verify")
    a = verify(bounty)
    bounty = pickle.loads(bounty)
    safeprint("Internal verify")
    b = bounty.isValid()
    if a and b:
        with bountyLock:
            bountyList.append(bounty)
    return (a and b)
