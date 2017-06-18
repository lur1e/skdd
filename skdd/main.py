from skdd import datatools

import sys
import skdd.core as core
import skdd.util as util

from skdd.config import logger


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'nasa.xlsx'

    tablecol = datatools.get_data(filename, view='col')
    tablerow = datatools.get_data(filename, view='row')
    print(tablecol)
    #print(tablerow)
    ncols = len(tablecol)
    nrows = 0
    if ncols:
         nrows = len(tablecol[0])
    if nrows:
         logger.info('Stats: rows: %s, columns: %s' % (nrows, ncols))
         H = core.smth(nrows)
         MH = core.smth_usl(nrows,H)
         print("MH:",MH)
         #valid_c_rules = core.columnrules(tablecol, nrows, 2, MH)
         #print("valid_c_rules:",valid_c_rules)
         list_valid_rules = []
         for col_ind in range(0, ncols):
             list_valid_rules.append(core.columnrules(tablecol, nrows, col_ind, MH))
         for ind, ind_v_rules in enumerate(list_valid_rules):
             print("rules for", ind, "arg: ", list_valid_rules[ind])



             #comb_list = util.combinations(ncols)

#
# xl_workbook = xlrd.open_workbook(file_name)
# xl_sheet = xl_workbook.sheet_by_index(0)
# print('Open Excel workbook %s, sheetname: %s' % (file_name, xl_sheet.name))
#
# ncols = xl_sheet.ncols  # Number of columns
# nrows = xl_sheet.nrows
#
# print('Stats: \n\t rows: %s, columns: %s' % (nrows, ncols))
# #util.printsheet(xl_sheet)
# comb_list = util.getallcomb(ncols)
# # logic.q_inf(xl_sheet, 0, 0)