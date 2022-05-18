from globalElements.setup import load

from globalElements import csvImporter

 
if __name__ == '__main__':
    importer = csvImporter.csvImporter()
    importer.avdtBookkeepingAdd()
