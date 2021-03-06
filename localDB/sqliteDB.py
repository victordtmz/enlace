import sqlite3
import os
 
oneDrive = os.path.expanduser('~\OneDrive')
class avdtLocalDB():
    def __init__(self):
        # self.configDB()
        # self.sqlFolder = 'localDB\sql'
        self.database = 'avdt.db' 
        self.dbFolder = f'{oneDrive}\db\oth\localDB' 

    def createSqliteConnection(self): 
        self.connection = sqlite3.connect(f'{self.dbFolder}\{self.database}')
        self.cursor = self.connection.cursor()
        
    def executeQuery(self, sql, var=0):
        self.createSqliteConnection()
        if var:
            self.cursor.execute(sql, var)
        else:
            self.cursor.execute(sql)
        self.connection.close()
    
    def executeQueryCommit(self, sql):
        self.createSqliteConnection()
        self.cursor.execute(sql)
        self.connection.commit() 
        self.connection.close()

    def executeQueryCommitReturnId(self, sql):
        self.createSqliteConnection()
        self.cursor.execute(sql)
        self.connection.commit() 
        idvar = self.cursor.lastrowid
        self.connection.close()
        return idvar

    def selectRecords(self, sql):
        self.createSqliteConnection()
        records = self.cursor.execute(sql)
        records = records.fetchall()
        self.connection.close()
        return records

    def selectOne(self, sql):
        self.createSqliteConnection()
        records = self.cursor.execute(sql)
        records = records.fetchone()
        self.connection.close()
        return records

    def selectRecordsAndLabels(self, sql):
        self.createSqliteConnection()
        records = self.cursor.execute(sql)
        records = records.fetchall()
        labelsInfo = self.cursor.description
        self.connection.close()
        labels = []
        for label in labelsInfo:
            labels.append(label[0])
        return (records, labels)

    # def getSQL(self, file):
    #     filePath = f"{self.sqlFolder}\{file}"
    #     sqlFile = open(filePath, "r")
    #     sqlFileText = sqlFile.read()
    #     sqlFile.close()
    #     return sqlFileText

    def insertNewRecord(self,sql):
        '''record is passed as a tuple with id'''
        idVar = self.executeQueryCommitReturnId(sql)
        # idVar = idVar[0][0]
        
        return idVar

    def deleteOne(self, table, idName, id_):
        sql = f'''DELETE FROM {table} WHERE {idName} = "{id_}";'''
        self.executeQueryCommit(sql)


if __name__ == '__main__':
    db = avdtLocalDB()
    