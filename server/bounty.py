from common import bounty

"""Contains overrides to the common.bounty package to deal with server-specific functions"""


def verify(string):
    """External method which checks the Bounty as valid under implementation-specific requirements. This can be defined per user.
    ip      -- Must be in valid range
    btc     -- Must be in valid namespace
    reward  -- Must be in valid range
    timeout -- Must be greater than the current time
    """
    from common.bounty import verify
    verify(string)
# The following is an identical copy of the common.bounty one. To change specifics, uncomment it.
#    test = string
#    if type(test) == type(""):
#        test = pickle.loads(string)
#    try:
#        safeprint("Testing IP address",verbosity=1)
#        if not checkIPAddressValid(test.ip):
#            return False
#        safeprint("Testing Bitcoin address",verbosity=1)
#        address = str(test.btc)
#        #The following is a soft check
#        #A deeper check will need to be done in order to assure this is correct
#        if not checkBTCAddressValid(address):
#            return False
#        safeprint("Testing reward",verbosity=1)
#        reward = int(test.reward)
#        boolean = reward >= 1440 and reward <= 100000000
#        if reward == 0 or reward is None or test.data.get('cert'):
#            safeprint("Testing signature validity",verbosity=1)
#            boolean = test.checkSign()
#        if boolean is False:
#            return False
#        safeprint("Testing timeout",verbosity=1)
#        if test.timeout < getUTC(): #check against current UTC
#            return False
#        from common.call import parse
#        safeprint("Testing bounty requirements",verbosity=1)
#        if parse(test.data.get('reqs')):
#            return 1
#        else:
#            return -1
#    except:
#        return False


def addBounty(bounty):
    """Verify a bounty, and add it to the list if it is valid"""
    from common.bounty import addBounty
    addBounty(bounty)
# The following is an identical copy of the common.bounty one. To change specifics, uncomment it.
#    first = False
#    safeprint([sys.version_info[0],sys.version_info[1],sys.version_info[2]])
#    if sys.version_info[0] == 2 and sys.version_info[1] == 6 and (type(bounty) == type("aaa") or type(bounty) == type(unicode("aaa"))):
#        safeprint("Fed as string in 2.6; encoding ascii and ignoring errors")
#        try:
#            bounty = bounty.encode('ascii','ignore')
#        except:
#            bounty = str(bounty)
#    elif type(bounty) == type("aaa") and sys.version_info[0] >= 3:
#        safeprint("Fed as string; encoding utf-8")
#        bounty = bounty.encode('utf-8')
#    safeprint(pickle.loads(bounty))
#    safeprint("External verify",verbosity=1)
#    try:
#        bounty = pickle.loads(bounty)
#    except:
#        return False
#    first = verify(bounty)
#    safeprint("Internal verify")
#    second = bounty.isValid()
#    if not second:
#        rval = -3
#    elif not first:
#        rval = -2
#    elif bounty in getBountyList():
#        rval = -1
#    elif second == -1:
#        rval = 0
#    else:
#        rval = 1
#    if rval == 1:
#        addValidBounty(bounty)
#    return rval
