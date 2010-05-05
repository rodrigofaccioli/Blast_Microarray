import os
import sys
from xlrd import open_workbook,XL_CELL_TEXT

header = ['MetaColumn', 'MetaRow', 'Column', 'Row', 'Reporter Identifier', 'Reporter Name', 'Reporter BioSequence Database Entry [beebase]', 'Reporter BioSequence Database Entry [entrez]', 'Reporter BioSequence Type', 'Reporter BioSequence PolymerType', 'Reporter BioSequence [Actual Sequence]', 'Reporter Comment', 'Reporter Group [Role]', 'Reporter Control Type']

def show_row(sh,rx):
    result = []
    colrange = range(sh.ncols)    
    ctys = sh.row_types(rx)
    cvals = sh.row_values(rx)
    for colx in colrange:
        cty = ctys[colx]
        cval = cvals[colx]
        result.append((colx, cty, cval))
    return result

   
def readFileXLS(path, filename):
    pathfilename = os.path.join(path, filename)
    book = open_workbook(pathfilename)
    sh = book.sheet_by_index(0)
    rowsrange = range(sh.nrows)

    header = []
    dicRet = {}
    for rx in rowsrange:
        Values = []
        for colx, ty, val in show_row(sh, rx):
            if rx == 0:
                val = str(val)
                header.append(val)
            else:
                if colx == 4:
                    key = str(val)
                if colx == 5:
                    val = str(val).split()[0] #Only GB.
                else:
                    val = str(val)
                Values.append(val)
        if rx > 0:
            dicRet[key] = Values
    return dicRet
                

def createTXTFile(dicValues, pathtxtfileName):
    file_txt = open(pathtxtfileName, "w")
    #Create Header
    h = ""
    for c in header:
        h1 = "%s" %str(c)
        h = str(h) + str(h1) + " "
    h = str(h) + "\n"
    file_txt.write(h)
    #Create lines
    for k, values in dicValues.iteritems():
        line = ""
        for v in values:
            v1 = "%s" %str(v)
            line = str(line) + str(v1) + " "
        line = str(line) + "\n"
        file_txt.write(line)
    file_txt.close()
    
def main():
    path = sys.argv[1] #Path for files
    filename = sys.argv[2] #xls file name
    txtfileName = sys.argv[3] #txt file name
    
    #Read XLS file and build the dictionary and header for txt file
    header = [] 
    dicValues = {}
    dicValues = readFileXLS(path, filename)
    #Create txt file
    pathtxtfileName = os.path.join(path, txtfileName)
    createTXTFile(dicValues, pathtxtfileName) 
    
    
main()   
    
