import sys

import skdd.core as core

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'test.xlsx'

    core.analysis(filename)
