import os
from globalElements import DB
from localDB.sqliteDB import avdtLocalDB 

#prepare mysqlDb
avdtDB = ('u210833393_AVDT', 'u210833393_victorMtz', 'Abogado2020$')
traduccionesDB = ('u210833393_traducciones', 'u210833393_victor', 'Abogado2020$')
avdOld = ('u210833393_AVD','u210833393_VictorMartinez','Abogado2020')
mysqlDB = DB.DB(avdtDB[0], avdtDB[1], avdtDB[2])

#program paths
oneDrive = os.path.expanduser('~\OneDrive')
rootEnlace = f'{oneDrive}\enlace'
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
iconExcel = f"{iconsFolder}excel.png"
# # Carriers
# # ------------------------------------------------------------
# carriersDict = {}
# carriersList = []
# def queryCarriers():
#     sql = f'''SELECT 
#             id, 
#             IFNULL(name_,'')
#             FROM carriers 
#         ;'''
#     records = mysqlDB.get_records(sql)
#     carriersDict.clear()
#     carriersDict[""] = 0
#     for i in records:
        
#         carriersDict[i[1]] = i[0]
#         carriersList.append(i[1])

# clients
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

# trucks
# ------------------------------------------------------------
trucksDict = {}
trucksList = []
def queryTrucks():
    sql = f'''SELECT 
            id, 
            IFNULL(no_,'')
            FROM trucks 
        ;'''
    records = mysqlDB.get_records(sql)
    trucksDict.clear()
    trucksDict[""] = ""
    for i in records:
        trucksDict[i[1]] = i[0]
        trucksList.append(i[1])

# trailers
# ------------------------------------------------------------
trailersDict = {}
trailersList = []
def queryTrailers():
    sql = f'''SELECT 
            id, 
            IFNULL(no_,'')
            FROM trailers 
        ;'''
    records = mysqlDB.get_records(sql)
    trailersDict.clear()
    trailersDict[""] = ""
    for i in records:
        trailersDict[i[1]] = i[0]
        trailersList.append(i[1])

# drivers
# ------------------------------------------------------------
driversDict = {}
driversList = []
def queryDrivers():
    sql = f'''SELECT 
            id, 
            IFNULL(name_,'')
            FROM drivers 
        ;'''
    records = mysqlDB.get_records(sql)
    driversDict.clear()
    driversDict[""] = ""
    for i in records:
        driversDict[i[1]] = i[0]
        driversList.append(i[1])

# agents
# ------------------------------------------------------------
agentsDict = {}
agentsList = []
def queryAgents():
    sql = f'''SELECT 
            id, 
            IFNULL(name_,'')
            FROM clients_agents 
        ;'''
    records = mysqlDB.get_records(sql)
    agentsDict.clear()
    agentsDict[""] = ""
    for i in records:
        agentsDict[i[1]] = i[0]
        agentsList.append(i[1])

# bookkeeping categories
# ------------------------------------------------------------
bookkeepingTruckingCategoriesDict = {}
bookkeepingTruckingCategoriesList = []
def querybookkeepingTruckingCategories():
    sql = f'''SELECT 
            id, 
            IFNULL(categorie,'')
            FROM bookkeeping_categories 
            WHERE industry = "Trucking"
        ;'''
    records = mysqlDB.get_records(sql)
    bookkeepingTruckingCategoriesDict.clear()
    bookkeepingTruckingCategoriesDict[""] = ""
    for i in records:
        bookkeepingTruckingCategoriesDict[i[1]] = i[0]
        bookkeepingTruckingCategoriesList.append(i[1])

# bookkeeping Industries
# ------------------------------------------------------------
bookkeepingTruckingIndustries = []
def querybookkeepingTruckingIndustries():
    sql = f'''SELECT DISTINCT
            IFNULL(industry,'')
            FROM bookkeeping_categories;'''
    records = mysqlDB.get_records(sql)
    for i in records:
        bookkeepingTruckingIndustries.append(i[0])


#g! Local db items
#--------------------------------------------------------------
localDB = avdtLocalDB()
# Schedule C
scheduleItems = []
scheduleDict = {}
scheduleCompleteDict = {}
def queryScheduleC():
    sql = f'''
        SELECT * FROM scheduleC;
    '''
    records = localDB.selectRecords(sql)
    scheduleItems.append('')
    scheduleDict[''] = ''
    for i in records:
        scheduleItems.append(i[1])
        scheduleDict[i[1]] = i[0]
        scheduleCompleteDict[0] = [i[1],i[2],i[3]]

# Accounts
accountsItems = []
accountsDict = {}
def queryAccounts():
    sql = f'''
        SELECT idCarrier, account FROM bAccounts;
    '''
    records = localDB.selectRecords(sql)
    accountsItems.append('')
    accountsDict[''] = ['']
    for i in records:
        accountsItems.append(i[1])
        if i[0] not in accountsDict.keys():
            accountsDict[i[0]] = [i[1]]
        else:
            accountsDict[i[0]].append(i[1])

# carriers
carriersItems = []
carriersDict = {}
def queryCarriers():
    sql = f'''
        SELECT idCarrier, carrier FROM carriers;
    '''
    records = localDB.selectRecords(sql)
    carriersItems.append('')
    carriersDict[''] = ''
    for i in records:
        carriersItems.append(i[1])
        carriersDict[i[1]] = i[0]

# months
monthsItems = []
def queryMonths():
    sql = f'''
        SELECT * FROM months_;
    '''
    records = localDB.selectRecords(sql)
    monthsItems.append('')
    for i in records:
        monthsItems.append(i[0])

# years
yearsItems = []
def queryYears():
    sql = f'''
        SELECT * FROM years_;
    '''
    records = localDB.selectRecords(sql)
    for i in records:
        yearsItems.insert(0, i[0])
    yearsItems.insert(1, '')

# years
iftaJuris = []
def queryIftaJuris():
    sql = f'''
        SELECT * FROM jurisdictions;
    '''
    records = localDB.selectRecords(sql)
    for i in records:
        iftaJuris.insert(0, i[0])
    iftaJuris.insert(1, '')



