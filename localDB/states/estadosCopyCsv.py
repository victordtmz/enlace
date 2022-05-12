from asyncio import constants
from email import header
from reprlib import recursive_repr
from localDB import sqliteDB
from globalElements.functions import getRecordsFromCSV

class DB(sqliteDB.avdtLocalDB):
    def __init__(self):
        super().__init__()
        # id, state_, city
        self.database = 'mex.avd'

    def importFromCsv(self):
        file = f'{self.dbFolder}\\mex.csv'
        records, header = getRecordsFromCSV(file)
        return records
    
    def insertRecords(self):
        records = self.importFromCsv()
        a = '''--sql'''
        sql = f'''
        INSERT INTO estados (state_,city) VALUES {records};
        '''
        self.executeQueryCommit(sql)

    def createTable(self):
        a = '''--sql'''
        sql = '''
        CREATE TABLE IF NOT EXISTS estados (
            id INTEGER PRIMARY KEY,
            state_ TEXT,
            city TEXT
            );
        '''
        self.executeQuery(sql)
    

if __name__ == '__main__':
    db = DB()
    db.sh
    

    