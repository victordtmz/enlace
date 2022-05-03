from globalElements import DB, constants, functions

class Clone():
    def __init__(self):
        pass

    def cloneDB(self):
        dbLogin = constants.avdOld
        dataBase = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        sql = f'''
            SELECT 
                *
            FROM AVDT_Accounting_Loads;
        '''
        records = dataBase.get_records_clearNull(sql)


        # records = functions.recordToSQL(records)

        dbLogin = constants.avdtDB
        dataBase = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        for r in records:
            r = functions.recordToSQL(r)
            sql = f'''INSERT IGNORE INTO bookkeeping_loads 
            (idBookkeeping, idLoads) VALUES 
            ({r[0]},{r[1]})'''
            try:
                dataBase.run_sql_commit(sql)
            except:
                continue
        
        # records = str(records)
        # records = records.replace('[','(')
        # records = records.replace(']',')')
        # records = records[1:-1]
        # # print(records)
        # # print(type(records))
        # sql = self.getSQL("avdt\\bookkeeping\\bookkeeping_loads\insertNewRecord.sql")
        # sql = f'{sql} {records};'
        # dbLogin = constants.avdtDB
        # dataBase = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        # dataBase.run_sql_commit(sql)

    def getSQL(self,file):
            # filePath = f"{self.sqlFolder}/{file}"
        sqlFile = open(file, "r")
        sqlFileText = sqlFile.read()
        sqlFile.close()
        return sqlFileText
