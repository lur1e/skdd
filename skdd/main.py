import sys
import skdd.core as core

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'nasa.xlsx'

    vr = core.analysis(filename)
    for ind, ind_v_rules in enumerate(vr):
        print("--Rules for", ind, "arg: ", vr[ind])