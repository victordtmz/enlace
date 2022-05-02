import sqlite3
from globalElements import constants

class DB():
    def __init__(self):
        self.configDB()
        
    def configDB(self):
        self.sqlFolder = 'sqlite\zipCodes'
        self.database = 'name.avd'
    
    def createSqliteConnection(self, db):
        dbFolder = f'{constants.othFolder}\localDB'
        self.connection = sqlite3.connect(f'{dbFolder}\{db}')
        self.cursor = self.connection.cursor()
        
    def executeQuery(self, sql):
        self.createSqliteConnection(self.database)
        self.cursor.execute(sql)
        self.connection.close()
    
    def executeQueryCommit(self, sql):
        self.createSqliteConnection(self.database)
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def selectRecords(self, sql):
        self.createSqliteConnection(self.database)
        records = self.cursor.execute(sql)
        records = records.fetchall()
        self.connection.close()
        return records

    def selectRecordsAndLabels(self, sql):
        self.createSqliteConnection(self.database)
        records = self.cursor.execute(sql)
        records = records.fetchall()
        labelsInfo = self.cursor.description
        self.connection.close()
        labels = []
        for label in labelsInfo:
            labels.append(label[0])
        return (records, labels)

    def getSQL(self, file):
        filePath = f"{self.sqlFolder}\{file}"
        sqlFile = open(filePath, "r")
        sqlFileText = sqlFile.read()
        sqlFile.close()
        return sqlFileText


if __name__ == '__main__':
    db = DB()
    