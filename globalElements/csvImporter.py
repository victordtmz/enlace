from globalElements.setup import logger
from globalElements import constants, DB
from globalElements import functions

class csvImporter():
    def __init__(self) -> None:

        dbC = constants.avdtDB
        self.db = DB.DB(dbC[0], dbC[1],dbC[2])
        self.lg = logger()
        self.logger = self.lg.logger

    def getRecords(self):
        self.csvFilePath = f'{constants.oneDrive}\AVDTrucking\Carriers\AVD TRUCKING LLC\Accounting\CSVFormats_Accounts'
        self.csvFileName = 'BofA.csv'
        csvFile = f'{self.csvFilePath}\{self.csvFileName}'
        records, header, noRecords = functions.getRecordsFromCSV(csvFile)
        return records, noRecords

    def avdtBookkeepingAdd(self):
        records, noRecords = self.getRecords()

        sql = f'''INSERT INTO bookkeeping 
            (idCarrier, idCategorie, account_, date_, amount, 
            isIncome, description_, anexo, isBusiness) VALUES {records}'''

        self.db.run_sql_commit(sql)
        self.logger.info(f"Added {noRecords} to AVDT Accounting DB from {self.csvFileName}")

    def __repr__(self) -> str:
        return '''
        csvImporter --> takes values from a CSV file and inserts new records into mysql table in the DB
        '''
        





    