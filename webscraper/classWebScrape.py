import csv
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import parse_qs, urlparse

class webScrape:
    def __init__(self):
        self.__url = ""
        self.__subUrl = ""
        self.__unit1 = ""
        self.__unit2 = ""
        self.__citiesDict = {}
        self.__outFl = ""
        self.__outputFileHeader = ["Code", "Location", "Registered", "Envelopes", "Valid"]
    

    def checkUrlAvailable(self, url):
        retVal = False
        webResponse = requests.get(url)
        if webResponse.status_code == 200:
            self.__url = url
            self.parseUrl() # parsing url for suburl
            retVal = True
        return(retVal)
    

    def parseUrl(self):
        parsedUrl = urlparse(self.__url)
        # get unit1 param xkraj
        self.__unit1 = parse_qs(parsedUrl.query).get('xkraj', [None][0])[0]
        # get unit2 param xnumnuts
        self.__unit2 = parse_qs(parsedUrl.query).get('xnumnuts', [None][0])[0]
        #print(self.__unit1)
        #print(self.__unit2)


    def scrapeUrl(self, method, code):
        match method:
            case "getCitiesCodes":
                webResponse = requests.get(self.__url)
                soup = bs(webResponse.text, features='html.parser')
                numbers = tuple(a.text for a in soup.find_all("td", class_="cislo"))
                cities = tuple([td.text] for td in soup.find_all("td", class_="overflow_name"))
                self.__citiesDict = dict(zip(numbers, cities))
            case "getPoliticPartyNames":
                self.__subUrl = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={self.__unit1}&xobec={code}&xvyber={self.__unit2}"
                webResponse = requests.get(self.__subUrl)
                soup = bs(webResponse.text, features='html.parser')
                # scraping politic party names 1 bez bordela
                politicPartyNames1 = tuple(td.text.strip().replace("\xa0", "") for td 
                                      in soup.find_all('td', {'headers': 't1sa1 t1sb2'}) 
                                      if (not td.text.strip().replace("\xa0", "") == "-"))
                # scraping politic party names 2 bez bordela
                politicPartyNames2 = tuple(td.text.strip().replace("\xa0", "") for td 
                                      in soup.find_all('td', {'headers': 't2sa1 t2sb2'}) 
                                      if (not td.text.strip().replace("\xa0", "") == "-"))
                self.__outputFileHeader.extend(politicPartyNames1)
                self.__outputFileHeader.extend(politicPartyNames2)
            case "getCityResults":
                retVal = []
                self.__subUrl = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={self.__unit1}&xobec={code}&xvyber={self.__unit2}"
                webResponse = requests.get(self.__subUrl)
                soup = bs(webResponse.text, features='html.parser')
                # scraping registered
                registered = soup.find('td', {'headers': 'sa2'}).text.strip().replace("\xa0", "")
                # scraping envelopes
                envelopes = soup.find('td', {'headers': 'sa3'}).text.strip().replace("\xa0", "")
                # scraping valid
                valid = soup.find('td', {'headers': 'sa6'}).text.strip().replace("\xa0", "")
                # scraping politic party table 1 bez bordela
                politicParty1 = tuple(td.text.strip().replace("\xa0", "") for td 
                                      in soup.find_all('td', {'headers': 't1sa2 t1sb3'}) 
                                      if (not td.text.strip().replace("\xa0", "") == "-"))
                # scraping politic party table 2 bez bordela
                politicParty2 = tuple(td.text.strip().replace("\xa0", "") for td 
                                      in soup.find_all('td', {'headers': 't2sa2 t2sb3'}) 
                                      if (not td.text.strip().replace("\xa0", "") == "-"))
                retVal.append(registered)
                retVal.append(envelopes)
                retVal.append(valid)
                retVal.extend(politicParty1)
                retVal.extend(politicParty2)
                return(retVal)


    def getCities(self):
        self.scrapeUrl("getCitiesCodes", 0)


    def getElectionCitiesResults(self):
        counter = 0        
        for code, cities in self.__citiesDict.items():
            if(counter == 0): # run just once to create outputfile header
                self.scrapeUrl("getPoliticPartyNames", code)
            scrapedData = self.scrapeUrl("getCityResults", code)
            cities.extend(scrapedData)
            counter += 1
        

    def createOutputDataFile(self):
        retval = True # be nice by default...
        try:
            with open(self.__outFl, mode='w', newline='') as file:
                writer = csv.writer(file) # writer object
                writer.writerow(self.__outputFileHeader) # write header
                for code, statistics in self.__citiesDict.items(): # write all data rows
                    statistics.insert(0, code)
                    writer.writerow(statistics)
        except Exception as e:
            retval = False
            print(f"Method createOutputDataFile() with exception: {e}")
        return(retval)


    # getters, setters a jina hejblata
    def setOutputFileName(self, value):
        if(isinstance(value, str)):
            self.__outFl = value
