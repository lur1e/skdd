import timeit
import math
import itertools
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

# q_inf([1,1,2],2)

def smth(row_count):
    d = {}
    for el in range(1, row_count + 1):
        # print(el)
        size_part = util.partition(el)
        MH = 0
        for part in size_part:
            ExpH = 0
            logger.debug("Next partition: "+ str(part))
            # print(part)
            H = 0
            for value in part:
                H += q_inf(part, value)
            H /= len(part)
            if H == 0:
                ExpH = 0
            else:
                P = p_coef(part)
                #   print(H,P)
                ExpH = H * P
            # print(ExpH)
            MH += ExpH
            #   print("MH:",MH)
        d[el] = MH
    return d


def p_coef(extended_part):
    n = len(extended_part)
    k = len(Counter(extended_part).keys())
    logger.debug("    k:"+ str(k))
    p = 1
    number_of_elements = Counter(extended_part).values()
    logger.debug("    NOE:"+ str(number_of_elements))
    for pc in number_of_elements:
        logger.debug("    p:"+ str(pc))
        p *= math.factorial(pc)
    s = 1
    number_of_v = Counter(list(Counter(extended_part).values())).values()
    for sc in number_of_v:
        logger.debug("    s:"+ str(sc))
        s *= math.factorial(sc)
    logger.debug("    n:"+ str(n))
    result = math.factorial(n) * math.factorial(n) / ((n ** n) * math.factorial(n - k) * p * s)
    logger.debug("    "+ str(result))
    logger.debug("    ----------------------------------")
    return result


def smth_usl(row_count, dH):
    l = util.accel_asc(row_count)
    MH = 0
    for part in l:
        Mpart = 0
        for num in part:
            p = num / row_count
            Exp = p * dH[num]
            #   print(p, dH[num],Exp)
            Mpart += Exp
        # print(Mpart)
        p = p_coef(util.extended_part(part))
        expPart = p * Mpart
        MH += expPart
    # print(MH)
    return MH

def columnrules(tablecol, nrows, arg_ind):
    logger.debug("Column rules start")
    maincol = tablecol[arg_ind]
    len_maincol = len(maincol)
    prob = {}
    rules = {}
    unique_args = set(maincol)
    for value in unique_args:
        prob[value] = maincol.count(value) / len_maincol
    logger.debug("Column rules, prob = "+str(prob))
    #generate rules
    rules = util.generate_rules(len(tablecol),arg_ind)
    for rule in rules:
        #list of columns in rule
        col_Idx = [int(c_column[:-1]) for c_column in rule] #index is integer
        #print("col_Idx:", col_Idx)
        # unique self-rule
        ruletable = []
        if len(col_Idx) == 1 and col_Idx[0] == arg_ind:
            logger.debug("Column rules; Detected self-rule: " +str(col_Idx[0])+"rule = "+str(arg_ind)+
                         "arg")
            ruletable = [q_inf(tablecol[arg_ind],value) for value in unique_args]
        else:
            #print(nrows)
            rules_rows = (list(list(tablecol[col_ind][row_ind] for col_ind in col_Idx) for row_ind in range(0, nrows)))
            #print(rules_rows)
            unique_rr = util.dedup(rules_rows)
            #print(unique_rr)
            for rulerow in unique_rr:
                ruletablerow=[]
                for arg in unique_args:
                    #вычисляем количество информации для конкретного аргумента конкретной строки правила
                    qi = q_inf_table(tablecol,nrows,rulerow,col_Idx,arg, arg_ind)
                    ruletablerow.append(qi)
                    #print("row:",rulerow, "args:",arg)
                ruletable.append(ruletablerow)
        print(ruletable)
        print("---------------------------------------------------------")
    logger.debug("Column rules end")

def q_inf_table(tablecol, nrows, rulerow, col_Idx, arg, arg_ind):
    #print("строк:", nrows, "правило", rulerow, "индексы правила:", col_Idx, "arg: ",arg, "arg_ind:",arg_ind)
    #start
    #check only col_Idx columns
    base = 0 # number of table[row] at col_Idx and rulerow
    value = 0 # number of args equals at base rows
    for row_ind in range(0,nrows): #for every row in table
        # check equals between rulerow and table[row] in col_Idx indexes
        if [tablecol[col_ind][row_ind] for col_ind in col_Idx] == rulerow:
            #print([tablecol[col_ind][row_ind] for col_ind in col_Idx], rulerow)
            base += 1
            if tablecol[arg_ind][row_ind] == arg: #count value
                value += 1
    #print(base, value, arg)
    if value == 0 or base == 0:
        return 0
    l = 1
    if not (base == 1 and value == 1):
        l = math.log(value, base)
    return l

    # logger.debug("log(base:",base,", value:",value,") =", l,
    #              "for rulerow:", str(rulerow),
    #              "and arg:", arg)

        #for col_ind in col_Idx:
        #    print(tablecol[col_ind][row_ind], "[",row_ind, col_ind,"]",rulerow)
    # print(smth(4))
    # smth_usl(5, {})
    # p = [1,2,2,3,3,4]
    # print(Counter(p).values())
    # print(Counter(list(Counter(p).values())).values())
    # print(timeit.timeit("math.factorial(100)", "import math"))
