def call(mod, cmd, *args, **kargs):
    """Calls arbitrary python code

    Arguments:
        mod     - The module from which you are calling
        cmd     - The command in said module
        *args   - Any arguments you need to give to it
        index=0 - A specific index at which to return
        end=0   - An end range from which to return
    Use case:
        if you don't know what command you need to run at compile time
    """
    m = __import__(mod)
    func = getattr(m, cmd)
    if not isinstance(func, type(open)) and not isinstance(func, type(call)):
        r = func
    else:
        r = func(*args)
    index = kargs.get('index')
    if index is not None:
        end = max(index + 1, kargs.get('end'))
        return r[index:end]
    else:
        return r


def process(tup):
    """Convert tuples into a format readable by call.call"""
    args = []
    ix = None
    ex = None
    for item in tup[0]:
        if isinstance(item, str):
            if item[:6] == "index=":
                ix = int(item[6:])
            elif item[:4] == "end=":
                ex = int(item[4:])
            else:
                args.append(item)
        else:
            args.append(item)
    args = tuple(args)
    a = call(*args, index=ix, end=ex)
    return a == tup[1]


def parse(d):
    """Check a dict keyed by the related calls against their expected values
    Dict format:
        Key:
            tuple:
                [0]     - module from which the command is called
                [1]     - command which you are calling
                [*]     - index=x, where x is the index you wish
                [*]     - end=x, where x is the end of the range to return
                [*]     - all other args in the order the command is supposed
                            to receive it; keyed arguments are not supported
        Value:
            The expected return value
    """
    if d == {} or d is None:
        return True
    if len(d) == 1:
        return process(list(d.items())[0])
    from multiprocessing.pool import ThreadPool
    p = list(d.items())
    r = ThreadPool().map(process, p)
    return not (False in r)
