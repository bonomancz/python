
"""
ODBC connection, query class
Uses pyodbc module.
Author: Jan Novotny (2024)
Mail: jan.novotny.cz@gmail.com
"""

import pyodbc

class DBOdbc():
    
    def __init__(self):
        ''' default constructor '''
        self.connection = None
        self.cursor = None

    
    def connect(self, connectionString):
        ''' ODBC connect function '''
        retVal = False
        try:
            self.connection = pyodbc.connect(connectionString)
            self.cursor = self.connection.cursor()
            retVal = True
        except pyodbc.Error as e:
            print(f"Method: connect(): Exception: {e}")
            retVal = False
            raise e
        return retVal


    def query(self, queryString):
        ''' ODBC send query function '''
        retVal = None
        try:
            print(self.getQueryType(queryString))
            if self.cursor.execute(queryString):
                retVal = self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Method: query(): Exception: {e}")
            retVal = None
            raise e
        return retVal
    

    def disconnect(self):        
        ''' ODBC close function '''
        retVal = False
        if self.connection:
            if self.connection.close():
                retVal = True
        return retVal


    def getQueryType(self, queryString):
        retVal = ""
        keyWord = queryString.split(" ")
        retVal = keyWord[0]
        return retVal
