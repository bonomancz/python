"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Jan Novotny (2024)
email: bonoman@volny.cz
discord: Bonoman#0823
"""

import sys
from classWebScrape import webScrape

# main function
def main(url, outFile):
    retVal = True
    ws = webScrape()
    ws.setOutputFileName(outFile) # setting constructor filename
    if(not ws.checkUrlAvailable(url)): # trying http 200 OK or die tcp !!!!!
        retVal = False
        quit("URL not available. Quit.")
    print("Scraping URL.")
    ws.getCities() # scraping cities codes, names
    print("Scraping election details in cities. This may take some time. Please be patient.")
    ws.getElectionCitiesResults() # scraping cities details
    print("Creating output data file.")
    if(not ws.createOutputDataFile()): # preparing output file
        retVal = False
        quit("Preparing output data file failed. Contact you system administrator.")
    print("Finished.")
    return(retVal)


# print program usage
def printUsage():
    retVal = "\nUsage example: projekt_3.py [url] [output_file.csv]"
    return(retVal)


# if running as standalone script
if __name__ == "__main__":
    if(not len(sys.argv) == 3):
        quit("Application needs minimum 2 parameters. Quit.")
    else:
        url = sys.argv[1]
        outputFile = sys.argv[2]
        if not "https://" in url:
            quit("Invalid URL format. Quit" + printUsage())
        if not ".csv" in outputFile:
            quit("Invalid CSV name. Quit" + printUsage())


# run, run, run...
main(url, outputFile)
