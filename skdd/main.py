from skdd import datatools

import sys
import skdd.core as core
import skdd.util as util

from skdd.config import logger


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'test.xlsx'

    table = datatools.get_data(filename)
    nrows = len(table)
    ncols = 0
    if nrows:
         ncols = len(table[0])
    if ncols:
         logger.info('Stats: rows: %s, columns: %s' % (nrows, ncols))
         H = core.smth(nrows)
         core.smth_usl(nrows,H)
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