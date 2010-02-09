from Bio.Blast import NCBIXML
import sys

def readxml(filenamexml):
    #This functions reads all a Blast XML file 
    E_VALUE_THRESH = 0.04
    result_handle = open(filenamexml)
    blast_records = NCBIXML.parse(result_handle)
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

def main():
    filenamexml = sys.argv[1]
    readxml(filenamexml)
    print "Done"
    
main()

  
    