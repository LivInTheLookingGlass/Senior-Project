from common.bounty import Bounty


def validation():
    """Validate the Bounty class's definition checker"""
    # Currently does not check certificate validity
    # This could be done in two steps
    # 1. Form the unsigned bounty
    # 2. Add to the data field the correct sig, key, cert
    l = []
    num_completely_invalid = 8
    num_invalid = num_completely_invalid + 2
    # Begin adding to check-list
    l += [(Bounty(('8.8.8.8', -1), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1440),
          "Bounty with invalid ip address (invalid port)")]
    l += [(Bounty(('8.8.8', 8888), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1440),
          "Bounty with invalid ip address (incorrect number of bytes)")]
    l += [(Bounty(('8.8.8.8', 49153), "1111111111111111111114oLvT2", 1440),
          "Bounty with invalid ip address (invalid port)")]
    l += [(Bounty(('8.8.256.8', 8), "1111111111111111111114oLvT2", 1440),
          "Bounty with invalid ip address (overflowed byte in address)")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGGww4ZEDmP7u9", 1440),
          "Bounty with invalid bitcoin address")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1439),
          "Bounty with invalid reward amount (outside of valid range)")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 0),
          "Bounty with invalid reward amount (reward of zero with no sig)")]
    l += [(Bounty(('8.8.8.8', 8), "1111111111111111111114oLvT2", 1440, timeout=1),
          "Bounty that has timed out")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1440,
                  data={'reqs': {("sys", "platform", "index=2",
                                 "end=3"): "win33"}}),
          "Bounty with invalid requirements (would not work on any system")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1440,
                  data={'reqs': {("__builtin__", "pow", 2, 2): 4,
                                 ("sys", "platform"): "w"}}),
          "Bounty with invalid requirements (including some valid ones)")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1440),
          "Correctly formed bounty")]
    l += [(Bounty(('8.8.8.8', 8), "1LhPsd4ng3AXmVPzrLWprWFx351pW4HJm8", 10900),
          "Correctly formed bounty")]
    l += [(Bounty(('8.8.8.8', 8), "1MWSdYMKEpfWVxC6BGYARxsksaQuyEWzG5", 1480),
          "Correctly formed bounty")]
    l += [(Bounty(('8.8.8.8', 8), "1EgGfDetymjMzcQ1AEhHjHEyXHjnEavwgg", 10290),
          "Correctly formed bounty")]
    l += [(Bounty(('8.8.8.8', 8), "1JTGcHS3GMhBGLcFRuHLk6Gww4ZEDmP7u9", 1440,
                  data={'reqs': {("__builtin__", "pow", 2, 2): 4}}),
          "Correctly formed bounty with system requirements")]
    # Begin testing list
    for i in range(len(l)):
        if bool(i >= num_completely_invalid) ^ bool(l[i][0].isValid()):
            return (False, l[i][1])
    return (True, "All bounties correctly assessed")
