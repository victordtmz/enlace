#!/usr/bin/python3

import queue
from mysql.connector import errors
import mysql.connector as mysql
from mysql.connector.locales.eng import client_error

class DB():
    def __init__(self):
        super().__init__()
        self.createConnection()
    def createConnection(self):
        self.dbConnection = mysql.connect(host='sql535.main-hosting.eu',
                                database='u210833393_AVD',
                                user='u210833393_VictorMartinez',
                                password='Abogado2020')
        self.cursor = self.dbConnection.cursor(buffered=True)
    
    def query(self, sql, parameters=""):
        '''PARA EJECUTAR SQL CUANDO NO EXISTEN VARIABLES - INFORMACION QUE CAMBIA SEGUN SE REQUIERA'''
        parameters = parameters
        try:
            self.cursor
            self.dbConnection
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)  # ERRO IS HERE / NOT EXCEPTING
        except errors.OperationalError:
            #     dbgLabel.config(text='RECONNECTION HAS TO BE ESTABLISHED FOR THE DB TO WORK /// error.OperationalError:')
            self.createConnection()
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)   # ERRO IS HERE / NOT EXCEPTING
    
    def query_records(self,sql, parameters=""):
        self.query(sql, parameters)
        records = self.cursor.fetchall()
        return records
    
    def run_sql_commit(self, sql):
        self.query(sql)
        sql = ('COMMIT;')
        self.query(sql)

    def insertNewRecord(self,sql):
        '''record is passed as a tuple with id'''
        self.run_sql_commit(sql)
        sql = '''SELECT LAST_INSERT_ID();'''
        idVar = self.query_records(sql)
        # idVar = db.DB_MySQL.cursor.fetchall()
        idVar = idVar[0][0]
        
        return idVar
    
    def deleteOne(self, table, idName, id_):
        sql = f'''DELETE FROM {table} WHERE {idName} = {id_};'''
        self.run_sql_commit(sql)

    def clearNull(self, records): #O! updated 
        recordsList = []
        for record in records:
            # recordsList.append(list(map(lambda i: '' if (i is None or i == "None") else str(i),record)))
            recordsList.append(list(map(lambda i: '' if (i is None) else str(i),record)))
        return recordsList

    def selectAll(self, table, sqlInput=''): #O! updated
        if sqlInput:
            sql = sqlInput
        else:
            sql = f'SELECT * FROM {table};'
        records = self.query_records(sql)
        recordsList = self.clearNull(records)
        return recordsList

    

DB_MySql = DB()

