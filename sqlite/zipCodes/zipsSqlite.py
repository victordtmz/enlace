from ast import Return
from sqlite import sqliteDB
class DB(sqliteDB.DB):
    def __init__(self):
        super().__init__()
        pass
        # ['zip-0', 'stateName-1', 'stateId-2', 'city-3', 'county-4', 'lat-5', 'lng-6']
        self.sqlFolder = 'sqlite\zipCodes'
        self.database = 'zips.avd'

    def selectZipCode(self, zipCode):
        sql = f'SELECT * FROM zipCodes WHERE ZIP = {zipCode};'
        records = self.selectRecords(sql)[0]
        return (records)

    def selectCityState(self, zipCode):
        record = self.selectZipCode(zipCode)
        return record[3], record[2]

    def selectStates(self):
        sql = f'''SELECT DISTINCT
            stateId
            FROM zipCodes
            ORDER BY stateId;'''
        records = self.selectRecords(sql)
        records = list(map(lambda x: x[0], records))
        return (records)

    def selectCities(self, state):
        sql = f'''SELECT DISTINCT
            city
            FROM zipCodes
            WHERE stateId = "{state}"
            ORDER BY city;'''
        records = self.selectRecords(sql)
        records = list(map(lambda x: x[0], records))
        return (records)

if __name__ == '__main__':
    db = DB()
    

    