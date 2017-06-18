import math
from collections import Counter

from skdd import util
from skdd.config import logger
import skdd.config as config

def q_inf(list, value):
    base = len(list)
    value = list.count(value)
    if base == 1 and value == 1:
        return config.log11
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
            logger.debug("Next partition: " + str(part))
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


def columnrules(tablecol, nrows, arg_ind, mh):
    logger.debug("Column rules start")
    maincol = tablecol[arg_ind]
    len_maincol = len(maincol)
    prob = {}
    unique_args = set(maincol)
    for value in unique_args:
        prob[value] = maincol.count(value) / len_maincol
    logger.debug("Column rules, prob = " + str(prob))
    # generate rules
    rules = util.generate_rules(len(tablecol), arg_ind)
    valid_rules = []
    for rule in rules:
        # list of columns in rule
        col_Idx = [int(c_column[:-1]) for c_column in rule]  # index is integer
        # print("col_Idx:", col_Idx)
        #TODO: unique self-rule actions
        ruletable = []
        if len(col_Idx) == 1 and col_Idx[0] == arg_ind:
            logger.debug("Column rules; Detected self-rule: " + str(col_Idx[0]) + "rule = " + str(arg_ind) +
                         "arg")
            ruletable = [q_inf(tablecol[arg_ind], value) for value in unique_args]
        else:
            # print(nrows)
            rules_rows = (list(list(tablecol[col_ind][row_ind] for col_ind in col_Idx) for row_ind in range(0, nrows)))
            # print(rules_rows)
            unique_rr = util.dedup(rules_rows)
            # print(unique_rr)
            for rulerow in unique_rr:
                ruletablerow = []
                for arg in unique_args:
                    # вычисляем количество информации для конкретного аргумента конкретной строки правила
                    qi = q_inf_table(tablecol, nrows, rulerow, col_Idx, arg, arg_ind)
                    ruletablerow.append(qi)
                    # print("row:",rulerow, "args:",arg)
                ruletable.append(ruletablerow)
            Hy = rule_properties(tablecol, nrows, unique_rr, col_Idx,
                                 unique_args, arg_ind, ruletable, rules_rows)
            #print(Hy)
            if Hy > mh:
                #TODO: узнать у Юли о дополнительной проверке
                logger.debug("   VALID!   rule:"+str(rule)+"  --  Hy > Mh:"+str(Hy)+">"+str(mh))
                valid_rules.append(rule)
            else:
                logger.debug("   rule:"+str(rule)+"  --  Hy < Mh:"+str(Hy)+"<"+str(mh))
        logger.debug("Column rules:"+str(ruletable)+" for rule: "+str(rule)+"-> "+str(arg_ind)+'c')
        logger.debug("Column rules: ---------------------------------------------------------")
        # print(ruletable)
        # print("---------------------------------------------------------")
    logger.debug("Column rules end")
    return valid_rules


def q_inf_table(tablecol, nrows, rulerow, col_Idx, arg, arg_ind):
    logger.debug("    Quantity of information in table start")
    # print("строк:", nrows, "правило", rulerow, "индексы правила:", col_Idx, "arg: ",arg, "arg_ind:",arg_ind)
    c_rulerow = count_rulerow(tablecol,nrows,rulerow,col_Idx,arg,arg_ind)
    value = c_rulerow['value']
    base = c_rulerow['base']
    # print(base, value, arg)
    if value == 0 or base == 0:
        logger.debug("    QoI: value == 0 or base == 0")
        logger.debug("    Quantity of information in table end")
        return 0
    l = config.log11
    if not (base == 1 and value == 1):
        l = math.log(value, base)
    logger.debug("    QoI: qoi = "+str(l)+
                 "; arg = "+str(arg)+
                 "; rulerow = "+str(rulerow)+";")
    logger.debug("    Quantity of information in table end")
    return l

def count_rulerow(tablecol, nrows, rulerow, col_Idx, arg, arg_ind):
    # start
    # check only col_Idx columns
    base = 0  # number of table[row] at col_Idx and rulerow
    value = 0  # number of args equals at base rows
    for row_ind in range(0, nrows):  # for every row in table
        # check equals between rulerow and table[row] in col_Idx indexes
        if [tablecol[col_ind][row_ind] for col_ind in col_Idx] == rulerow:
            # print([tablecol[col_ind][row_ind] for col_ind in col_Idx], rulerow)
            base += 1
            if tablecol[arg_ind][row_ind] == arg:  # count value
                value += 1
    return {"base": base, "value": value}

def rule_properties(tablecol, nrows, unique_rr, col_Idx, unique_args, arg_ind, ruletable, rules_rows):
    #doesn't work on self-property
    #print(unique_rr)
    #старт какой-то неверной жопы, спросить у Юли
    Hch = []
    for r_ind, rulerow in enumerate(unique_rr):
        h_row = 0
        for a_ind, arg in enumerate(unique_args):
            c_rulerow = count_rulerow(tablecol,nrows,rulerow,col_Idx,arg,arg_ind)
            #print(c_rulerow)
            cellinf = ruletable[r_ind][a_ind]
            #print(cellinf)
            h_row_el = ruletable[r_ind][a_ind]*(c_rulerow['value']/c_rulerow['base'])
            h_row += h_row_el
            # if cellinf:
            #     hrow+=
        #print("     ", r_ind, rulerow, h_row)
        Hch.append(h_row)
    #print(Hch)
    #конец какой-то неверной жопы
    #prob
    #TODO: внести в один цикл!!
    prob = []
    for r_ind, rulerow in enumerate(unique_rr):
        prob.append(rules_rows.count(rulerow) / nrows)
    #print(prob)
    #Exp
    Exp = [Hch[ind]*prob[ind] for ind in range(0, len(Hch))]
    #print(Exp)
    #Hy
    Hy = sum(Exp)
    #print("Hy:",Hy)
    return Hy


