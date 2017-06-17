import timeit
import math
from collections import Counter

from skdd.config import logger
from skdd import util

def q_inf(list, value):
    base = len(list)
    value = list.count(value)
    if base == 1 and value == 1:
        return 1
    l = math.log(value, base)
    logger.debug("log(base=%s, value=%s) = %s " % (base, value, l))
    return l

#q_inf([1,1,2],2)

def smth(row_count):
    d = {}
    for el in range(1, row_count+1):
        #print(el)
        size_part = util.partition(el)
        MH = 0
        for part in size_part:
            ExpH = 0
            logger.debug("Next partition: ", part)
            #print(part)
            H = 0
            for value in part:
                H += q_inf(part,value)
            H /= len(part)
            if H == 0:
                ExpH = 0
            else:
                P = p_coef(part)
             #   print(H,P)
                ExpH = H*P
            #print(ExpH)
            MH += ExpH
     #   print("MH:",MH)
        d[el] = MH
    return d

def p_coef(extended_part):
    n = len(extended_part)
    k = len(Counter(extended_part).keys())
    logger.debug("    k:", k)
    p = 1
    number_of_elements = Counter(extended_part).values()
    logger.debug("    NOE:", number_of_elements)
    for pc in number_of_elements:
        logger.debug("    p:",pc)
        p*=math.factorial(pc)
    s = 1
    number_of_v = Counter(list(Counter(extended_part).values())).values()
    for sc in number_of_v:
        logger.debug("    s:",sc)
        s *= math.factorial(sc)
    logger.debug("    n:",n)
    result = math.factorial(n) * math.factorial(n) / ((n ** n) * math.factorial(n-k) * p * s)
    logger.debug("    ",result)
    logger.debug("    ----------------------------------")
    return result

def smth_usl(row_count, dH):
    l = util.accel_asc(row_count)
    MH = 0
    for part in l:
        Mpart = 0
        for num in part:
            p = num/row_count
            Exp = p*dH[num]
         #   print(p, dH[num],Exp)
            Mpart+=Exp
        #print(Mpart)
        p = p_coef(util.extended_part(part))
        expPart = p*Mpart
        MH += expPart
    #print(MH)
    return MH






#print(smth(4))
#smth_usl(5, {})
# p = [1,2,2,3,3,4]
# print(Counter(p).values())
# print(Counter(list(Counter(p).values())).values())
#print(timeit.timeit("math.factorial(100)", "import math"))