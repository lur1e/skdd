import xlrd
from skdd.config import logger

def get_data(filename):
    logger.info("Getting file: "+filename)
    filetype = filename.rpartition('.')[-1]
    if filetype == "xlsx" or "xls":
        return excel_import(filename)
    return None

def excel_import(filename):
    l = []
    xl_workbook = xlrd.open_workbook(filename)
    xl_sheet = xl_workbook.sheet_by_index(0) #1st list only
    logger.info('Open Excel workbook %s, sheetname: %s' % (filename, xl_sheet.name))
    for row_ind in range(0, xl_sheet.nrows):
        l.append(xl_sheet.row_values(row_ind))
    logger.info(l)
    #printsheet(xl_sheet)
    return l

def printsheet(sheet):
    for row_idx in range(0, sheet.nrows):  # Iterate through rows
        print('-' * 40)
        print('Row: %s' % row_idx)  # Print row number
        for col_idx in range(0, sheet.ncols):  # Iterate through columns
            cell_obj = sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            print('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))
    print('-' * 40 + "\n" + '-' * 40 + '\n')
