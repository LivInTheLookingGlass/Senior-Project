from common import settings
import math, sys

possibilities = ["-c", "-f 4", "-o", "-p 44444", 
                 "-s", "-S", "-t", "-v", "-v", "-v"]
default = {'accept_latency': 2000,
           'charity': False,
           'outbound': False,
           'port': 44565,
           'propagate_factor': 2,
           'seed': False,
           'server': False,
           'test': False,
           'verbose': 0}


def accurateParsing():
    from common import safeprint
    safeprint.silent_flag.value = True
    for i in range(len(possibilities)):
        print(i)
        tests = genTests(i)
        for j in range(len(tests)):
            settings.config.update(default)
            settings.saveSettings()
            sys.argv = tests[j]
            ret = verify(math.factorial(i) + j, tests[j])
            if not ret:
                safeprint.silent_flag.value = False
                return ret
    safeprint.silent_flag.value = False
    return True


def genTests(i):
    from itertools import combinations
    tests = list(combinations(possibilities, i))
    for j in range(len(tests)):
        tests[j] = list(tests[j])
    removals = []
    for test in tests:
        if "-s" in test and "-S" in test:
            removals.append(test)
    for test in removals:
        tests.remove(test)
    return [sys.argv + test for test in tests]


def verify(i, test):
    settings.setup()
    ret = testToggles(test)
    # test verbosity
    ret = test.count("-v") == settings.config['verbose'] and ret    # test integer values
    return ret and testIntegers(test)


def testIntegers(test):
    ret = True
    for flag in test:
        if flag[0:3] == "-f ":
            ret = int(flag[3:]) == settings.config['propagate_factor']
            break
    for flag in test:
        if flag[0:3] == "-p ":
            ret = int(flag[3:]) == settings.config['port'] and ret
    return ret


def testToggles(test):
    ret = bool(test.count("-c")) == settings.config['charity']
    ret = bool(test.count("-o")) == settings.config['outbound'] and ret
    ret = bool(test.count("-s")) == settings.config['server'] and ret
    ret = bool(test.count("-S")) == settings.config['seed'] and ret
    ret = bool(test.count("-t")) == settings.config['test'] and ret
    return ret
