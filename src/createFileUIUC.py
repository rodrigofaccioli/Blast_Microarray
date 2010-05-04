import os

def getValue(listLine):
# Values are all file columns except AM columns which is the first. 
    r = ""
    GB = ""
    i = int(1) #Eliminate the first column (AM column) 
    while i < listLine.__len__():
        if str(listLine[i]).find("GB") >= 0:
            GB = str(listLine[i])
        else:
            r = r + " " + str(listLine[i])
        i = i + 1
    return str(GB).strip()+"#"+str(r).strip()
    
def createFileUIUC_READ_TO_WORK():
   #This function creates the UIUC_Honey_bee_oligo_READ_TO_WORK.txt file 
   # that is based on UIUC_HoneyBeeOligo.txt. The last file is a XLS version 
   # file from website.
   # it's used when XLS file changed
   path = "/home/faccioli/workspace/blast/BeeArray"
   filenameSource = "UIUC_HoneyBeeOligo.txt"  #Was generating manually
   filenameDest = "UIUC_Honey_bee_oligo_READ_TO_WORK.txt"
   pathfilename =  os.path.join(path,filenameSource)
   f = open(pathfilename)
   save_file = open(os.path.join(path,filenameDest), "w")
   dic = {}
   for line in f:
        s = line.split()
        if str(s[0]).find("AM") >= 0:
            dic[str(s[0])] = getValue(s)
   
   sortDic = dic.keys()
   sortDic.sort()
   #for key,value in dic.iteritems():
   for key in sortDic:
       value = dic[key]
       l = "%s>%s \n" % (key,value)      
       save_file.write(l) 
   save_file.close()
   f.close()


def main():
    createFileUIUC_READ_TO_WORK()
    
main()   
    