import itertools
from collections import Counter

import math

from skdd.config import logger

# generate all rules for number of columns
def combinations(ncols):
    l = list(range(0, ncols))
    comb_list = []
    for dilimeter in range(0, ncols):
        sublist = list(l)
        sublist.remove(dilimeter)
        comb_dilim = list()
        for L in range(0, len(sublist) + 1):
            for subset in itertools.combinations(sublist, L):
                if subset:
                    comb_dilim.append(subset)
        comb_list.append(comb_dilim)
    return comb_list


# generate all partiniton of number
def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]


# give extended partitions list of number
def partition(num):
    result = []
    for el in reversed(list(accel_asc(num))):
        result.append(extended_part(el))
    return result


def patition_coef(extended_part):
    n = len(extended_part)
    k = len(Counter(extended_part).keys())
    logger.debug("    k:" + str(k))
    p = 1
    number_of_elements = Counter(extended_part).values()
    logger.debug("    NOE:" + str(number_of_elements))
    for pc in number_of_elements:
        logger.debug("    p:" + str(pc))
        p *= math.factorial(pc)
    s = 1
    number_of_v = Counter(list(Counter(extended_part).values())).values()
    for sc in number_of_v:
        logger.debug("    s:" + str(sc))
        s *= math.factorial(sc)
    logger.debug("    n:" + str(n))
    result = math.factorial(n) * math.factorial(n) / ((n ** n) * math.factorial(n - k) * p * s)
    logger.debug("    " + str(result))
    logger.debug("    ----------------------------------")
    return result


# extended partition of number
def extended_part(part):
    element = []
    for key, value in enumerate(reversed(part)):
        element.extend(value * [key + 1])
    return element


# generate all rules with number of columns for col_ind column
def generate_rules(ncols, col_ind):
    logger.debug("Generate rules start")
    l = list(range(0, ncols))
    for value, key in enumerate(l):
        l[key] = str(value) + 'c'
    logger.debug("Generate rules, list of columns: " + str(l))
    rules = []
    sublist = list(l)
    sublist.remove(str(col_ind) + 'c')
    rules.append([str(col_ind) + 'c'])
    for L in range(0, len(sublist) + 1):
        for subset in itertools.combinations(sublist, L):
            if subset:
                logger.debug("Generate rules, next rule: " + str(list(subset)) + " -> " + str(col_ind) + 'c')
                rules.append(list(subset))
    logger.debug("Generated rules: " + str(rules))
    logger.debug("Generate rules end.")
    return rules  # list of lists


# remove dup from list: (when set() not working)
def dedup(list):
    new_k = []
    for elem in list:
        if elem not in new_k:
            new_k.append(elem)
    return new_k
