from common.call import call


def accuracy():
    """Tests the accuracy of call.call"""
    import math, sys
    l, r = [], []
    num_invalid = 4
    # test unkeyed arguments

    l += [("sys", "platform")]
    r += ["win33"]
    l += [("math", "pow", 4, 4)]
    r += [3]
    l += [("sys", "maxint")]
    r += [-2]
    l += [("__builtin__", "max", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)]
    r += [9]
    l += [("__builtin__", "max", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)]
    r += [10]
    l += [("math", "pow", 5, 8)]
    r += [math.pow(5, 8)]
    l += [("sys", "platform")]
    r += [sys.platform]
    l += [("sys", "maxint")]
    r += [sys.maxint]

    for i in range(len(l)):
        if bool(call(*l[i]) == r[i]) ^ bool(i >= num_invalid):
            return False

    # test keyed arguments
    if ((call("sys", "platform", index=0) != sys.platform[0]) or
       (call("sys", "platform", index=2, end=3) != sys.platform[2:3])):
        return False

    return True
