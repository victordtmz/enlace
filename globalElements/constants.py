import os
from globalElements import DB

#prepare mysqlDb
avdtDB = ('u210833393_AVDT', 'u210833393_victorMtz', 'Abogado2020$')
avdOld = ('u210833393_AVD','u210833393_VictorMartinez','Abogado2020')
mysqlDB = DB.DB(avdtDB[0], avdtDB[1], avdtDB[2])

#program paths
oneDrive = os.path.expanduser('~\OneDrive')
rootDb = f'{oneDrive}\db'
othFolder =f'{rootDb}\oth'
#AVDT Root folders
rootAVDT = f'{oneDrive}\AVDTrucking'
# rootCarriersAVDT = f'{rootAVDT}\Carriers'
# iconsFolder = f'{othFolder}/icons'

#avdt DB


#icons
#----------------------------------------------
iconsFolder = f"{rootDb}\oth\icons\\"
iconClearFilter = f"{iconsFolder}clear-filter.png"
iconEraser = f"{iconsFolder}eraser.png"
iconRefresh = f"{iconsFolder}refresh.png"
iconNewRecord = f"{iconsFolder}add-file.png"
iconFolder = f"{iconsFolder}folder-horizontal-open.png"
iconDelete = f"{iconsFolder}trash.png"
iconToday = f"{iconsFolder}today.png"
iconLink = f"{iconsFolder}link.png"
iconFolderOpen = f"{iconsFolder}open-folder.png"
iconClose = f"{iconsFolder}close.png"
iconSave = f"{iconsFolder}diskette.png"
iconCancel = f"{iconsFolder}prohibition.png"
iconAdd = f"{iconsFolder}add.png"
iconTruck = f"{iconsFolder}truck.png"
iconJuicios = f"{iconsFolder}balance.png"
iconTranslate = f"{iconsFolder}translation.png"
iconCalculator = f"{iconsFolder}bank-account.png"
iconMoneyBag = f"{iconsFolder}moneyBag.png"
iconClient = f"{iconsFolder}client.png"
iconAccounts = f"{iconsFolder}user.png"
iconAccounting = f"{iconsFolder}accounting.png"
iconCategories = f"{iconsFolder}categories.png"
iconFuel = f"{iconsFolder}fuel.png"
iconDriver = f"{iconsFolder}driver.png"
iconTrailer = f"{iconsFolder}trailer.png"
iconCarrier = f"{iconsFolder}carrier.png"
iconWeb = f"{iconsFolder}internet.png"
iconCopy = f"{iconsFolder}copy.png"
iconCustomer = f"{iconsFolder}customer.png"
iconRoad = f"{iconsFolder}road.png"
iconWarehouse = f"{iconsFolder}warehouse.png"
iconIfta = f"{iconsFolder}IFTA.png"

# Carriers
# ------------------------------------------------------------
carriersDict = {}
carriersList = []
def queryCarriers():
    sql = f'''SELECT 
            id, 
            IFNULL(name_,'')
            FROM carriers 
        ;'''
    records = mysqlDB.get_records(sql)
    carriersDict.clear()
    carriersDict[""] = ""
    for i in records:
        
        carriersDict[i[1]] = i[0]
        carriersList.append(i[1])

# clientsAgents
# ------------------------------------------------------------
clientsDict = {}
clientsList = []
def queryClients():
    sql = f'''SELECT 
            id, 
            IFNULL(name_,'')
            FROM clients 
        ;'''
    records = mysqlDB.get_records(sql)
    clientsDict.clear()
    clientsDict[""] = ""
    for i in records:
        clientsDict[i[1]] = i[0]
        clientsList.append(i[1])
