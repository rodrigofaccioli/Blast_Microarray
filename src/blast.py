from Bio.Blast import NCBIWWW#
from Bio.Blast import NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import Bio.Alphabet
import sys
import os

CONFIGURE = {} #Dictionary for read parameters
LOGFILE = "File.log"
NO_MATH_FILE = "NoMatch.txt"
AM_WITHOUT_BLAST_FILE = "AM_withOut_Blast.txt"
#OFFICIAL_GENE_SET = "OfficialGeneSet_Array.txt"
OFFICIAL_GENE_SET = "Amel_pre_release2_OGS_cds.fa"


def createFileApis_ArraySet_READ_TO_WORK():
   #This function creates the Apis_ArraySet_READ_TO_WORK.txt file 
   # that is based on Apis_ArraySet.txt file. The last file is a XLS version 
   # file from website.
   # it's used when XLS file changed   
   filename = "Apis_ArraySet.txt"  #Was generating manually
   f = open(filename)
   save_file = open("Apis_ArraySet_READ_TO_WORK.txt", "w")
   for line in f:
        s = line.split()
        l = "%s %s %s %s" % (s[0],s[1],s[2],os.linesep)
        save_file.write(l) 
   save_file.close()
   f.close()

def getCompletePathFilenameXML(filenamexml):
    path = os.path.join(os.getcwd(), "XML") 
    filenamexml = os.path.join(path, filenamexml)
    return filenamexml

def readxml(filenamexml):
    #This functions reads all a Blast XML file
    filenamexml = getCompletePathFilenameXML(filenamexml)
    E_VALUE_THRESH = 0.04
    result_handle = open(filenamexml)
    blast_records = NCBIXML.parse(result_handle)
    q = 0
    for blast_record in blast_records:
            for alignment in blast_record.alignments:
               for hsp in alignment.hsps:
                  if hsp.expect < E_VALUE_THRESH:
                      print '****Alignment****'
                      print 'sequence:', alignment.title
                      print 'length:', alignment.length
                      print 'e value:', hsp.expect
                      print hsp.query[0:75] + '...'
                      print hsp.match[0:75] + '...'
                      print hsp.sbjct[0:75] + '...'
    result_handle.close()
    
def obatinIndexColumn(listColumns,columnName):
    #obtain the index of columnName
    indicecollum = 0
    i = 0
    while (i < len(listColumns)):
       if ( str(listColumns[i]).upper() == columnName.upper()):
            indicecollum = i 
            i = len(listColumns) # forced to exit
       i = i + 1
    return int (indicecollum)   

def obtainColumnsFile(filename,amountBlast=1,titlecolumnBlast="Blast"):
    #obtain the columns of file
    # The columns are in first line, only
    ls = []
    f = open(filename)
    line = f.readline()
    ls = line.split()
    f.close()
    i = 0
    t = ""
    while (i < int(amountBlast)):
        t = titlecolumnBlast + str(i+1)
        ls.insert(len(ls)+1,t)
        i = i + 1
    return ls

def getGBFromFilename(pathFilename):
    #From _path obtain GB
    # in Linux / is separate of directory
    # /home/faccioli/workspace/blast/XML/GB17693-PA_AM10266.xml
    l = os.path.split(pathFilename) # splits the file name from the _path and returns the name and directory _path as a tuple
    filename = l[1]
    GB = str(filename).split("_")
    GB = str(GB[0])
    unicode(GB,'latin-1').encode('ascii') 
    return GB
    
def loadBlastDefault():
    #This function reads Blast_default File and load it in dictionary
    D1 = {}
    f = open("Blast_Default.txt")
    for l in f:
        s = str(l).split(";")
        D1[s[0]] = str(s[1]).strip()
    f.close()        
    return D1    

def loadAM_WithOut_Blast():
    #This function reads AM_WITHOUT_BLAST_FILE File and load it in dictionary
    D1 = {}
    f = open(AM_WITHOUT_BLAST_FILE)
    for l in f:
        s = str(l).strip()
        s = str(s).split(">")
        D1[s[0]] = str(s[1]).strip()
    f.close()        
    return D1
         
def readBlastResultsFile(pathXML,filenameTXT,columnSource,columnBlast1,columnGB):
    # This function gets blast amount
    D1 = {}
    s = []
    i = -1
    indicecollum = 0
    saveLogFile(LOGFILE,"")
    listColumns = obtainColumnsFile(filenameTXT,getParameter("amountBlastColumn"))
    indexSource  = obatinIndexColumn(listColumns, columnSource)
    indexGB       = obatinIndexColumn(listColumns, columnGB)
    pos = loadBlastDefault()
    AM_WithOut_Blast = loadAM_WithOut_Blast()
    f = open(filenameTXT)
    f.next() # First line isn't necessary
    for line in f:
       title = {}
       GB    = "" 
       s = line.split()
       AM = s[indexSource]
       if pos.has_key(AM): #load from blast default
           title[0] = pos.get(AM) 
           GB    = ""
       elif AM_WithOut_Blast.has_key(AM):
           title[0] = AM_WithOut_Blast[AM] 
           GB    = ""               
       else: # Seek XML file to find GB and Blast    
          filenameXML = seekFile(pathXML, AM)
          if (filenameXML != " "):
              title = getTitleOfBestBlast(filenameXML, getParameter("amountBlastColumn"))
              GB    = getGBFromFilename(filenameXML)
          else:
             message = "XML file no Exists "+ str(AM) 
             saveLogFile(LOGFILE,message,"a")
       i = i + 1      
       D1[i] = createNewLine(s,title,GB,indexGB)
    f.close() 
    saveTXTFile(listColumns,D1,filenameTXT)

def createNewLine(s,title2,GB,indexGB):
   # Add the GB value and title, because there are their column name
   # but their values aren't in the TXT file           
   j = 0
   l = 0
   s2 = []
   #Blasts columns are the last columns and their start from s last column  
   indexStartBlastColumns = len(s) + 1 
   while (l < len(s)+2): 
      if (l == indexStartBlastColumns): #title blasts
         for i in title2:
            s2.append(title2[i])
      elif (l == indexGB): # GB value
         s2.append(GB)
      else:
         s2.append(s[j])
         j = j + 1 #index for TXT file columns
      l = l + 1   #index for while     
   return s2

                    
def saveTXTFile(listColumns,D1,filenameTXT):
   filenameTXT_Source = filenameTXT
   filenameTXT = filenameTXT + ".aux" #Security 
   save_file = open(filenameTXT, "w")
# Write the columns in the file   
   s = ""
   for c in listColumns:
       s = s + str(c) + "#"
   s = s + os.linesep    
   save_file.write(s)
# Write the lines in the file
   i = 0
   while (i < len(D1)):
      s = "" 
      line = D1[i]
      for l in line: 
          s = s + str(l)+ "#"
      s = s + os.linesep   
      save_file.write(s)
      i = i + 1
   save_file.close()
#Delete the TXT file source and rename filenameTXT.aux with same name TXT file source
   os.remove(filenameTXT_Source)
   os.rename(filenameTXT, filenameTXT_Source)   
   
def seekFile(path,partofFileName):
    # Seeks a file given a _path and part of its name 
    for filename in os.listdir(path):
        source_file = os.path.join(path, filename)
        if (source_file.find(partofFileName) > -1):
            return source_file     
    return " "

def getTitleOfBestBlast(filenamexml,amount=1):
    # Return title of amount Blast from XML file
    # Amount default is 1
    try:
       i = 0
       D = {}
       title = ""
       result_handle = open(filenamexml)
       blast_records = NCBIXML.parse(result_handle)
       blast_record = blast_records.next()
       while (i < int(amount)): 
          title = blast_record.alignments[i].title 
          title = title.split("|")
          D[i] =  title[4] # Only name
          i = i + 1   
       return D  
    except:
       message = "Error on %s" %filenamexml  
       saveLogFile(LOGFILE, message, "a")
    result_handle.close()   
    return ""   

def saveLogFile(filename,message,mode="w"):
   save_file = open(filename, mode)
   save_file.write(message+"\n")
   save_file.close()


# ********************************* BLAST ******************************    
def getAmountBlast(filename,columnName):
    # This function gets blast amount   
    f = open(filename)
    i = -1
    indicecollum = 0
    D1 = {}    
    for line in f:
        if (i == -1): #obtain the index of columnName
                l = ""
                ls = line.split()
                while (i <= len(ls)):
                   if (ls[i] == columnName):
                      indicecollum = i 
                      i = len(ls) # forced to exit
                   i = i + 1
                i = -1      
        else: # Build the dictionary           
            s = line.split()
            D1[i] = s[indicecollum]
        i = i + 1
    f.close            
    return D1

def seekInUIUC_Honey_bee_oligo_READ_TO_WORK(filename,AMvalue):
    # This function seeks in UIUC_Honey_bee_oligo_READ_TO_WORK.txt. 
    # The seeking process is, look for first column which is AM value. If found second column is split by '#'. Hence,
    # the GB value and its report are obtained. When there is a GB    
    f = open(filename)
    for line in f:
        s = line.split(">")
        if (s[0] == AMvalue):
            GB, report = str(s[1]).split("#")
            return GB, report
    f.close()        
    return None, None

def seekInBeeGenomeFastaFile(filename,value):
    value = str(value).split("-")[0]
    handle = open(filename, "rU")
    for record in SeqIO.parse(handle, "fasta") :
        gbinFile = str(record.id).split("|")[2]
        gbinFile = str(gbinFile).split("-")[0]
        if gbinFile == value: #Compare the GBs 
             return record
    handle.close()
    return None

def seekInOfficialGeneSet_ArrayFile(filename,value):
    value = str(value).split("-")[0]
    handle = open(filename, "rU")
    for record in SeqIO.parse(handle, "fasta") :
        gbinFile = None
        if str(record.id).find("GB") >= 0:
            if OFFICIAL_GENE_SET == "OfficialGeneSet_Array.txt":
                gbinFile = str(record.id).split("-")[0]
            elif OFFICIAL_GENE_SET == "Amel_pre_release2_OGS_cds.fa":
                gbinFile = str(record.id).split("|")[2]
                gbinFile = str(gbinFile).split("-")[0] 
            if gbinFile == value: #Compare the GB's values 
                return record
    handle.close()
    return None


def renameFiles(fileName):
    dir,file = os.path.split(fileName)
    file = str(file).replace(":", "_")
    f = os.path.join(dir,file)
    #print f
    return f

def createFileFasta(filenameFasta,record):
    filenameFasta = renameFiles(filenameFasta)
    outFile = open(filenameFasta,"w")
    l = ">" + record.id + "\n"
    l = l + record.seq
    outFile.write(str(l))
    outFile.close()
    return filenameFasta
    
def blast(r,filenameFasta,path,Dic):
    # This function does a blast from a Fasta file with one sequence and 
    # its results will write on xml file which same Fasta name File
   filenamexml = r+"_"+Dic+".xml"
   database = getParameter("database")
   record = SeqIO.read(open(filenameFasta), "fasta")#parse(open(filenameFasta,"rU"), "fasta").next()
   result_handle = NCBIWWW.qblast(getParameter("programBlast"), database, record.seq)
   blast_results = result_handle.read()
   save_file = open(path+filenamexml, "w")
   save_file.write(blast_results)
   save_file.close()

def cleanFile(pathFileName):
    auxFile = open(pathFileName, "w")
    auxFile.close()
    
def saveFileNoMatch(filename,Oligo_ID,mode="w"):
   # This save contains the Oligo_ID which doesn't have match and
   # therefore no Blast
   save_file = open(filename, mode)
   save_file.write(Oligo_ID+os.linesep)
   save_file.close()

def saveFileAMWithOutBlast(filename,Oligo_ID,mode="w"):
   # This save contains the Oligo_ID which did not made blat because it does not have GB value
   # therefore no Blast
   save_file = open(filename, mode)
   save_file.write(Oligo_ID+os.linesep)
   save_file.close()

def initialize(path):
    #cleaning Files
    cleanFile(path+NO_MATH_FILE)
    cleanFile(path+AM_WITHOUT_BLAST_FILE)
    
def doBlast():
   # The main function
   print "starting"
   path = getParameter("pathBlast")
   D1 = getAmountBlast(getParameter("fileTXT"), getParameter("columnAM"))
   i = 0
   initialize(path)
   while (i < len(D1)):
         GB, report = seekInUIUC_Honey_bee_oligo_READ_TO_WORK("UIUC_Honey_bee_oligo_READ_TO_WORK.txt",D1[i])
         if GB == None:
             message = str(D1[i]) + " " + "GB is None"
             saveFileNoMatch(path+NO_MATH_FILE, message,"a")
         elif GB.find("GB") >= 0 : # To do Blast when GB value was found. 
             print GB
             record = seekInOfficialGeneSet_ArrayFile(OFFICIAL_GENE_SET, GB)
             if (record != None):
                fileFasta = path+"fasta/"+GB+"_"+D1[i]+".fasta"
                fileFasta = createFileFasta(fileFasta, record)
                print "Blast %s " % i
                blast(GB, fileFasta, path+"XML/",D1[i])
             else:
                 message =  "%s %s GB does not found in %s" % (str(D1[i]), str(GB), OFFICIAL_GENE_SET)
                 saveFileNoMatch(path+NO_MATH_FILE, message,"a")
         else: # No Blast
             print "No Blast %s " % i
             value = D1[i] + ">" + str(report).strip()
             saveFileAMWithOutBlast(path+AM_WITHOUT_BLAST_FILE, value,"a")
         i = i + 1
   print "Done"
   
def loadConfigure():
    filename = open("Configure.conf")
    for l in filename:
        s = str(l).split("=")
        key = str(s[0]).strip()
        CONFIGURE[key] = str(s[1]).strip()
    filename.close()    

def getParameter(paramName):
    if CONFIGURE.has_key(paramName):
        return str(CONFIGURE.get(paramName))
    else:
        raise "Parameter %s not Found" % paramName

def displayXMLFileAmountBlast(filenameXML,amount):
    #Shows only title from XML file Blast
    # The display quantity is amount 
    filenameXML = getCompletePathFilenameXML(filenameXML)  
    D = getTitleOfBestBlast(filenameXML, amount)
    print "Read alignments title from XML Blast file %s " % getParameter("fileXML")
    print "-----------------------------------------------------------------------"
    for i in D:
        print D[i]
        
def main():
    loadConfigure()
    if getParameter("optionRun") == "doBlast":
         doBlast()
    elif getParameter("optionRun") == "readBlastResultsFile":
        readBlastResultsFile(getParameter("pathXML"),getParameter("fileTXT"),getParameter("columnAM"), getParameter("columnBlast"),getParameter("columnGB"))
    elif getParameter("optionRun") == "readxml":
        readxml(getParameter("fileXML"))
    elif getParameter("optionRun") == "createApis_ArraySet_READ_TO_WORK":
        createFileApis_ArraySet_READ_TO_WORK()
    elif getParameter("optionRun") == "displayXMLFileAmountBlast":
        displayXMLFileAmountBlast(getParameter("fileXML"), getParameter("amountBlastDisplay"))
            
main()