
from distutils import ccompiler
import imp
from avdt import bookkeeping
from avdt.bookkeeping import categories
from sqlite import sqliteDB
from sqlite.scheduleC import scheduleC
from globalElements.widgets import cbo
from PyQt6.QtWidgets import QCompleter
from PyQt6.QtCore import Qt

class scheduleCbo(cbo):
    def __init__(self, fontSize =13):
        super().__init__(fontSize)
        self.db = DB()
        self.db.selectListItems()
        completer = QCompleter(self.db.list)
        # completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setCompleter(completer)
        self.addItems(self.db.list)
        self.currentValues = []
        # self.currentTextChanged.connect(self.populateCurrentValues)

    def populateCurrentValues(self):
        item = self.getInfo()
        record = self.db.selectByItem(item)[0]
        self.currentValues = record
        # or i in record:
        #     self.currentValues.append(i[0])

    def getDbInfo(self):
        v = self.getInfo()
        sql = f'''
            SELECT id from {self.db.tableName}
            WHERE item = '{v}' ORDER BY item
        ''' 
        info = self.db.selectRecords(sql)[0][0]
        return info

class DB(sqliteDB.DB):
    def __init__(self):
        super().__init__()
        pass
        #'id-0', 'item-1', 'itemEs-2', 'itemDesc-3'
        self.sqlFolder = 'sqlite\scheduleC'
        self.database = 'scheduleC.avd'
        self.tableName = 'scheduleC'
        self.id_ = 'id'
        self.dict = {}
        self.dictCbo = {}
        self.list = []

    def selectListItems(self):
        sql = f'''
            SELECT item FROM {self.tableName}
        '''
        records = self.selectRecords(sql)
        self.list.append('')
        for i in records:
            self.list.append(i[0])
    
    def selectDict(self):
        self.dict[""] = ""
        self.dictCbo[""] = ""
        records = self.selectAll()
        for i in records:
            self.dict[i[0]] = [i[1],i[3],i[2]]
            self.dictCbo[i[0]] = i[1]

    def selectByItem(self, txt):
        sql = f'''
            SELECT * FROM {self.tableName}
            WHERE item = '{txt}'
        '''
        records = self.selectRecords(sql)
        return records

    def selectAll(self):
        sql = f'''
            SELECT * FROM {self.tableName}
        '''
        records = self.selectRecords(sql)
        return records

    def createDB(self):
        records = []
        for k,v in scheduleC.scheduleC.items():
            record = [k]
            for i in v:
                record.append(i)
            records.append(record)
        sql = self.getSQL('createTable.sql')  
        self.executeQuery(sql) 
        for i in records:
            sql = f'''INSERT INTO scheduleC 
                (id, item, itemEs, itemDesc)
            VALUES ("{i[0]}", "{i[1]}", "{i[2]}", "{i[3]}")
        '''
            self.executeQueryCommit(sql)

if __name__ == '__main__':
    db = DB()
    

    