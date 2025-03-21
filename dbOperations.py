# Moduuli Postgresql tietokantapalvelimen käyttämiseen
import psycopg2

import json

import cipher

import datetime

# Luokat
class DbConnection():
    def __init__(self, settings: dict):
        self.settings = settings
        self.server = settings['server']
        self.port = settings['port']
        self.databaseName = settings['database']
        self.userName = settings['userName']
        self.password = settings['password']
        
        # Yhteysmerkkijono
        self.connectionString = f'dbname={self.databaseName} user={self.userName} password={cipher.decryptString(self.password)} host={self.server} port={self.port}'

    # Metodi tietojen lisäämiseen (INSERT)
    def addToTable(self, table: str, data: dict) -> str:

        # Muodostetaan lista sarakkeiden (kenttien) nimistä ja arvoista SQL lausetta varten
        keys = data.keys() # Luetaan sanakirjan avaimet
        columns = ''
        values = ''

        for column in keys:
            columns += column + ', '
            rawValue = data[column]

            # Lisätään puolilainausmerkit, jos kyseessä on merkkijono
            if isinstance(rawValue, str):
                value = f'\'{rawValue}\'' # \' mahdollistaa puolilainausmerkin lisääminen
            else:
                value = f'{rawValue}'

            values += value + ', ' # Lisätään arvo sekä pilkku ja välilyönti

        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantaoperaatiota
            cursor = currentConnection.cursor()

            # Poistetaan viimeinen pilkku
            columns = columns[:-2]
            values = values[:-2]

            sqlClause = f'INSERT INTO {table} ({columns}) VALUES ({values})'
            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuman (transaction)
            currentConnection.commit()


        except(Exception, psycopg2.Error) as e:
            raise e
        
        finally:
            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    def readAllColumnsFromTable(self, table: str) -> list:
        records = []
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantaoperaatiota
            cursor = currentConnection.cursor()

            sqlClause = f'SELECT * FROM {table}'
            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)
            records = cursor.fetchall()
            return records

        except(Exception, psycopg2.Error) as e:
            raise e
        
        finally:
            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys


    def readChosenColumnFormTable(self, table, columns):
        records = []
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantaoperaatiota
            cursor = currentConnection.cursor()

            sqlClause = f'SELECT {columns} FROM {table}'
            
            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)
            records = cursor.fetchall()

        except(Exception, psycopg2.Error) as e:
            raise e
        
        finally:
            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

        return records
    
    def filterColumnsFromTable(self, table: str, columns: list, filter: str):
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()

            columnString = ''
            for column in columns:
                columnString += column + ', '

            cleanedColumnString = columnString[:-2]

            sqlClause = f'SELECT {cleanedColumnString} FROM {table} WHERE {filter};'
            cursor.execute(sqlClause)
            records = cursor.fetchall()
            return records
        
        except(Exception, psycopg2.Error) as e:
            raise e
        
        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    
    def modifyTableData(self, table: str, columnOfChange: str, newValue, lookForColumn, lookForValue):
        try:
            cuurrentConnection = psycopg2.connect(self.connectionString)
            cursor = cuurrentConnection.cursor()
            sqlClause = f'UPDATE {table} SET {columnOfChange} = {newValue} WHERE {lookForColumn} = {lookForValue}'
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuman (transaction)
            cuurrentConnection.commit()
        except(Exception, psycopg2.Error) as e:
            raise e
        
        finally:
            if cuurrentConnection:
                cursor.close()
                cuurrentConnection.close()

if __name__ == '__main__':

    testiasetukset = {"server": "127.0.0.1", "port": "5432", "database": "autolainaus", "userName": "autolainaus", "password": "gAAAAABnpGftFOtj6nvknyzBYXRw-mdPn9JcLc6jqE5_9639RYTsabBrkH7H9A5FlhqMVCrC2zcSllPX6TIXZXuirj3JVmj-dQ=="}
    dbConnection = DbConnection(testiasetukset)
   
    """ testidata = {'ryhma': 'Mopo Jopo',
                 'vastuuhenkilo': 'Hannu'}
    dbConnection.addToTable('ryhma', testidata) """

    '''taulukonSisältö = dbConnection.readAllColumnsFromTable('lainaaja')
    valitutKolumnit = dbConnection.readChosenColumnFormTable('lainaaja', 'hetu, sukunimi, etunimi')
    print(taulukonSisältö)
    print(valitutKolumnit)
    simpleList = []
    for tuple in valitutKolumnit:
            simpleList.append(tuple[0])
    print(simpleList)
  
    print(f'{datetime.datetime.now()}+02')
    dbConnection.modifyTableData('lainaus', 'palautus', 'CURRENT_TIMESTAMP', 'rekisterinumero', "'4567UI'")'''

    filterData = dbConnection.filterColumnsFromTable('ajossa', ['hetu', 'lainausaika'], "rekisterinumero = '5678OP'")
    print(filterData[0][0])