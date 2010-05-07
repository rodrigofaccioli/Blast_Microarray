import os
import sys
from xlrd import open_workbook,XL_CELL_TEXT

header = ['MetaColumn', 'MetaRow', 'Column', 'Row', 'Reporter Identifier', 'Reporter Name', 'Reporter BioSequence Database Entry [beebase]', 'Reporter BioSequence Database Entry [entrez]', 'Reporter BioSequence Type', 'Reporter BioSequence PolymerType', 'Reporter BioSequence [Actual Sequence]', 'Reporter Comment', 'Reporter Group [Role]', 'Reporter Control Type']
sequenceAM = [] #Store the sequence of AM values inserted from CSV file.

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
        h = str(h) + str(h1) + "\t"
    h = str(h) + "\n"
    file_txt.write(h)
    #Create lines
    for key in sequenceAM:
        line = ""
        # Dictionaries change the order of object. So, the AM values inserted ordered must
        # be inserted in same order. 
        values = dicValues[key]
        i = 0
        lenValues = values.__len__() 
        for v in values:            
            v1 = "%s" %str(v)
            line = str(line) + str(v1)
            if i < lenValues-1:
                line = str(line) + "\t"
            i = i + 1
        line = str(line)
        file_txt.write(line)
    file_txt.close()

   
def obtainGB(value):
    retValue = ""
    if (str(value).startswith("GB") ):
        retValue = str(value).split()[0]
    elif str(value).startswith("DB"):
        retValue = str(value).split()[0]
    elif str(value).startswith("BB"):
       retValue = str(value).split()[0]
    elif str(value).startswith("[Antisense]"):
        retValue = str(value).split()[1]
    else:
        retValue = value
    return str(retValue) 
        
    
def readFileCSV(path, filename):
    pathcsvfileName = os.path.join(path, filename)
    file_csv = open(pathcsvfileName, "r")
    dicRet = {}
    ki = -1
    for line in file_csv:
        ki = ki + 1
        valuesRes = []
        values = str(line).split(";")
        i = 0
        for v in values:
            if i == 4:
                #AM values are repeated. Therefore, the key 
                # must be AM + i
                key = str(v) + str(ki) 
                valuesRes.append(v)
                sequenceAM.append(key)
            elif i == 5:
                #Obtain GB without Blast information
                GB = str(obtainGB(v))
                valuesRes.append(GB)
            else:
                valuesRes.append(str(v))
            i = i + 1
        dicRet[key] = valuesRes
    return dicRet
    
def main():
    path = sys.argv[1] #Path for files
    filename = sys.argv[2] #CSV file name
    txtfileName = sys.argv[3] #txt file name
    
    #Read CSV file and build the dictionary and header for txt file
    header = [] 
    dicValues = {}
    #dicValues = readFileXLS(path, filename)
    dicValues = readFileCSV(path, filename)
    #Create txt file
    pathtxtfileName = os.path.join(path, txtfileName)
    createTXTFile(dicValues, pathtxtfileName) 
    
    
main()   
    
