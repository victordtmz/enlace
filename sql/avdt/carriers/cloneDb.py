from traceback import print_tb
from globalElements import DB, constants, functions

def cloneDB():
    dbLogin = constants.avdOld
    dataBase = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
    sql = f'''
        SELECT 
            IdCarrier,
            name_,
            MC,
            USDOT,
            EIN,
            Agent,
            phone, 
            address_,
            address_1,
            city,
            state_, 
            zip,
            Notas
        FROM AVDT_Carriers;
    '''
    records = dataBase.get_records_clearNull(sql)


    # records = functions.recordToSQL(records)

    
    for l in records:
        l = functions.recordToSQL(l)
    records = str(records)
    records = records.replace('[','(')
    records = records.replace(']',')')
    records = records[1:-1]
    # print(records)
    # print(type(records))
    sql = getSQL("avdt/carriers/insertNewRecord.sql")
    sql = f'{sql} {records};'
    dbLogin = constants.avdtDB
    dataBase = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])


    dataBase.run_sql_commit(sql)

def getSQL(file):
        # filePath = f"{self.sqlFolder}/{file}"
    sqlFile = open(file, "r")
    sqlFileText = sqlFile.read()
    sqlFile.close()
    return sqlFileText
