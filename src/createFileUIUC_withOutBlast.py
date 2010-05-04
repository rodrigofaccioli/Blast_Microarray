import os
import sys

def patternLine(line):
    #This function removes some characters such as "
    removeCharacters = ('"')
    for c in removeCharacters:
        line = str(line).replace(str(c), "") 
    return line
        
def createFileUIUC_WithOut_Blast(path):
   #This function creates the UIUC_Honey_bee_oligo__WithOut_Blast.txt file 
   # that is based on UIUC_HoneyBeeOligo.txt. The last file is a XLS version 
   # file from website.
   # it's used when XLS file changed and need to build a new txt file (table) without Blast column 
   filenameSource = "UIUC_HoneyBeeOligo.txt"  #Was generating manually
   filenameDest = "UIUC_Honey_bee_oligo_WithOut_Blast.txt"
   pathfilename =  os.path.join(path,filenameSource)
   f = open(pathfilename)
   save_file = open(os.path.join(path,filenameDest), "w")
   dic = {}
   for line in f:
        s = line.split()
        if str(s[0]).find("AM") >= 0:
            dic[str(s[0])] =  patternLine(str(s[1]))
   
   sortDic = dic.keys()
   sortDic.sort()
   for key in sortDic:
       value = dic[key]
       l = "%s>%s \n" % (key,value)      
       save_file.write(l) 
   save_file.close()
   f.close()


def main():
    path = sys.argv[1] #Path for files
    createFileUIUC_WithOut_Blast(path)
    
main()   
    
