from localDB import sqliteDB

class DB(sqliteDB.avdtLocalDB):
    def __init__(self):
        super().__init__()
        # id, state_, city
        self.database = 'us.avd'

    def selectEstados(self, pais):
        self.database = pais
        a = '''--sql'''
        sql = '''
        SELECT DISTINCT state_ FROM estados;
        '''
        records = self.selectRecords(sql)
        records = list(map(lambda x: x[0], records))
        print(records)
        return records

    def selectCiudades(self, pais, estado):
        self.database = pais
        a = '''--sql'''
        sql = f'''
        SELECT DISTINCT city FROM estados WHERE state_ = '{estado}';
        '''
        records = self.selectRecords(sql)
        records = list(map(lambda x: x[0], records))
        print(records)
        return records

    

if __name__ == '__main__':
    db = DB()
    

    