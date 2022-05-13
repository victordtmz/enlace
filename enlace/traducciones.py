#!/usr/bin/python3

from globalElements import DB, constants, modelMain
from globalElements.widgets import (buttonWidget, cbo, dateWidget, labelWidget,  lineEditCurrency, lineEditPhone, spinbox, 
    textEdit, lineEdit, cboFilterGroup, checkBox, truFalseRadioButtons, radioButtons)
import sys
import os
import pathlib
from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg 
import locale 
from localDB.sqliteDB import avdtLocalDB
locale.setlocale(locale.LC_ALL,"")
from decimal import *
from datetime import datetime

class estadosDB(avdtLocalDB):
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
        return records

    def selectCiudades(self, pais, estado):
        self.database = pais
        a = '''--sql'''
        sql = f'''
        SELECT DISTINCT city FROM estados WHERE state_ = '{estado}';
        '''
        records = self.selectRecords(sql)
        records = list(map(lambda x: x[0], records))
        return records


class tipoRadioButtons(radioButtons):
    def __init__(self, style = False):
        super().__init__(style)
        self.setTitle("Tipo")
        self.nacimiento = qtw.QRadioButton("Nacimiento")
        self.defuncion = qtw.QRadioButton("Defuncion")
        self.antecedentes = qtw.QRadioButton("Antecedentes")
        self.divorcio = qtw.QRadioButton("Divorcio")
        self.identificacion = qtw.QRadioButton("Identificacion")
        self.matrimonio = qtw.QRadioButton("Matrimonio")
         
        self.poder = qtw.QRadioButton("Poder")
        self.solteria = qtw.QRadioButton("Solteria")
        self.titulo = qtw.QRadioButton("Titulo")
        self.Otro = qtw.QRadioButton("Otro")# 
        self.default = qtw.QRadioButton("")# 

        self.itemsList.extend([self.nacimiento, self.defuncion, self.antecedentes, self.divorcio,
            self.identificacion, self.matrimonio, self.poder, self.solteria, self.titulo, self.Otro,
            self.default])
        # self.itemsList.append(self.Otro)
        # self.layout_ = qtw.QGridLayout()
        # self.layout_.setContentsMargins(0,0,0,0)
        #Row 0 
        self.layout_.addWidget(self.nacimiento,0,0)
        self.layout_.addWidget(self.defuncion,0,1)
        self.layout_.addWidget(self.antecedentes,0,2)
        self.layout_.addWidget(self.default,0,3)

        #Row 1
        self.layout_.addWidget(self.divorcio,1,0)
        self.layout_.addWidget(self.identificacion,1,1)
        self.layout_.addWidget(self.matrimonio, 1,2)

        #Row 2
        self.layout_.addWidget(self.poder,2,0)
        self.layout_.addWidget(self.solteria,2,1)
        self.layout_.addWidget(self.titulo,2,2)
        self.layout_.addWidget(self.Otro,2,3)

    def reSet(self):
        self.default.setChecked(True)

class dependenciaRadioButtons(radioButtons):
    def __init__(self, style = False):
        super().__init__(style)
        self.setTitle("Dependencia")
        self.regCivil = qtw.QRadioButton("Registro Civil")# 
        self.itemsList.append(self.regCivil)
        self.pJudicial = qtw.QRadioButton("Poder Judicial")
        self.itemsList.append(self.pJudicial)
        self.USCIS = qtw.QRadioButton("USCIS")# 
        self.itemsList.append(self.USCIS)
        self.Otro = qtw.QRadioButton("Otro")# 
        self.itemsList.append(self.Otro)
        self.default = qtw.QRadioButton("")# 
        self.itemsList.append(self.default)

        self.layout_.addWidget(self.Otro,0,3)
        self.layout_.addWidget(self.USCIS,0,2)
        self.layout_.addWidget(self.pJudicial,0,1)
        self.layout_.addWidget(self.regCivil,0,0)
        self.layout_.addWidget(self.default,0,0)

    def reSet(self):
        self.default.setChecked(True)

class idiomaRadioButtons(radioButtons):
    def __init__(self, style = False):
        super().__init__(style)
        self.setTitle("Idioma")
        self.ing = qtw.QRadioButton("Ingles")
        self.itemsList.append(self.ing)
        self.esp = qtw.QRadioButton("Español")
        self.itemsList.append(self.esp)

        self.layout_.addWidget(self.esp,0,1)
        self.layout_.addWidget(self.ing,0,0)

    def reSet(self):
        self.ing.setChecked(True)
    


class main(modelMain.main):
    def __init__(self):
        super().__init__()
        
        self.initUi()
        self.configure_form()
        self.configure_list()
        self.setConnections()
        self.listFontSize = 10
        self.requery()
        self.showMaximized()
        self.configureWidth()
        self.configureFormsFolder()

    def setGlobalVariables(self):
        # DB INFO
        self.size_ = "h1"
        self.idColumn = 'id' 
        self.tableVar = 'traducciones'
        self.listTableValuesIndexes = (0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)
        # self.formToDBItems = 4
        self.titleText = "TRADUCCIONES"
        # self.listExpand = 1
        # self.listExpand = 500
        # self.formExpand = 4
        self.widgetsOptSizes = [1,2]#list, form => relative size 
        # self.formExpand = 500
        self.listHiddenItems = (0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18)#(1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19)
        self.listColumnWidth = ((2,110),(3,300),(4,120))
        self.sortColumn = 1
        self.sortOrder = qtc.Qt.SortOrder.DescendingOrder
        self.onNewFocusWidget = 1
        dbLogin = constants.traduccionesDB
        self.db = DB.DB(dbLogin[0],dbLogin[1],dbLogin[2])
        a = '''--sql'''
        self.selectSql = '''
            SELECT 
                id, 
                folio AS "No",
                CONCAT(LPAD(folio,4,0), "/", YEAR(fecha)) as "Folio",
                titular AS  "Titular",
                tipo AS  "Tipo",
                fecha AS "Fecha",
                hojas AS "Hojas",
                costo AS "Costo",
                destino AS "Destino",
                idioma AS "Idioma",
                pais AS "Pais",
                estado AS "Estado",
                ciudad AS "Ciudad",
                origen AS "Dependencia",
                contacto AS "Solicitante",
                email AS "Email",
                telPais AS "Pais",
                telNo AS "Telefono",
                notas AS "Notas"
                FROM traducciones
                WHERE IFNULL (pais, "") LIKE %s
                AND IFNULL (estado, "") LIKE %s
                AND IFNULL (ciudad, "") LIKE %s
                AND IFNULL(tipo, "") LIKE %s
                AND YEAR(IFNULL(fecha, "")) LIKE %s
                ORDER BY fecha DESC, folio DESC
                LIMIT 400;
        '''
        a = '''--sql'''
        self.newRecordSql = ''' INSERT INTO traducciones (id, folio, titular, 
            tipo, fecha, hojas, costo, destino, idioma, pais, estado, ciudad, 
            origen, contacto, email, telPais, telNo, notas) VALUES '''
        a = '''--endsql'''
        
        # self.evaluateSaveIndex = (1,)
        # self.andOr = "and"
        

    def updateRecord(self, record): 
        a = '''--sql'''
        sql =f'''UPDATE traducciones SET 
                folio = '{record[1]}',
                titular = '{record[2]}',
                tipo = '{record[3]}',
                fecha = '{record[4]}',
                hojas = '{record[5]}',
                costo = '{record[6]}',
                destino = '{record[7]}',
                idioma = '{record[8]}',
                pais = '{record[9]}',
                estado = '{record[10]}',
                ciudad = '{record[11]}',
                origen = '{record[12]}',
                contacto = '{record[13]}',
                email = '{record[14]}',
                telPais = '{record[15]}',
                telNo = '{record[16]}',
                notas = '{record[17]}'
                WHERE id =  {record[0]};'''
        self.db.run_sql_commit(sql)

    def requery(self):
        qtw.QApplication.setOverrideCursor(qtg.QCursor(qtc.Qt.CursorShape.WaitCursor))
        pais = self.paisFilter.getInfo()
        if not pais: pais = '%'
        estado = self.estadoFilter.getInfo()
        if not estado: estado = '%'
        ciudad = self.ciudadFilter.getInfo()
        if not ciudad: ciudad = '%'
        tipo = self.tipoFilter.getInfo()
        if not tipo: tipo = '%'
        year = self.yearFilter.getInfo()
        if not year: year = '%'
        
        records = self.selectAll((pais, estado, ciudad, tipo, year))
        if records:
            self.list.requery(records, self.listFontSize, self.rowHeight, "Black")

            self.list.search_afterUpdate(self.sortColumn, self.sortOrder)
            self.list.proxyModel.sort(5, self.sortOrder)

        else:
            self.list.removeAllRows()
        
        self.configureColumns()
        while qtw.QApplication.overrideCursor() is not None:
            qtw.QApplication.restoreOverrideCursor()
        
        

    def btn_delete_pressed(self):
        record = self.list.treeview.selectionModel().selectedIndexes()
        
        #Verificar si hay registro seleccionado
        if record:
            idVar = self.id_.getInfo()
            folio = record[2].data()
            titular = record[3].data()
            text = f'''Delete load record:
            id: {idVar}
            Folio: {folio}
            Titular: {titular}'''
            self.deleteRecord(text)
        else:
            self.clearForm()
        
    def configure_form(self): 
        self.formLayoutTabsFilesTree()
        self.layoutFormBox.setMinimumWidth(450)
        self.layoutFormBox.setMaximumWidth(500)
        self.filesFolder.root = f'{constants.oneDrive}\Despacho\Traducciones\Traducciones'
        self.filesFolder.txtFilePath.setText(self.filesFolder.root)
        # self.title.deleteLater()
        self.titleLayoutBox.setMinimumHeight(40)

        self.setFormElements()

    def populateEstados(self):
        pais = self.pais.getInfo()
        db = estadosDB()
        if pais:
            estados = db.selectEstados(pais)
            estados.insert(0,'')
            self.estado.insertNewItems(estados)

    def populateCiudades(self):
        pais = self.pais.getInfo()
        estado = self.estado.getInfo()
        if pais and estado:
            db = estadosDB()
            ciudades = db.selectCiudades(pais, estado)
            ciudades.insert(0,'')
            self.ciudad.insertNewItems(ciudades)

    def populateOrigen(self):
        a = '''--sql'''
        sql = '''
            SELECT DISTINCT origen FROM traducciones
            WHERE pais LIKE %s
            AND estado LIKE %s
            AND ciudad LIKE %s;
        '''
        pais = self.pais.getInfo()
        if not pais: pais = '%'
        estado = self.estado.getInfo()
        if not estado: estado = '%'
        ciudad = self.ciudad.getInfo()
        if not ciudad: ciudad = '%'

        origenes = self.db.get_records_clearNull(sql, (pais,estado, ciudad))
        origenes = list(map(lambda x: x[0], origenes))
        origenes.append('')
        origenes.sort()
        origenes = set(origenes)
        self.origen.insertNewItems(origenes)
        

    def setFormElements(self):#p! Form elements
        self.id_ = lineEdit(self.fontSize)#
        self.id_.setReadOnly(True)
        self.folio = lineEdit(self.fontSize)
        self.titular = lineEdit(self.fontSize)
        self.tipo = tipoRadioButtons(True)
        self.fecha = dateWidget(self.fontSize)
        
        self.hojas = spinbox(self.fontSize)
        self.costo = lineEditCurrency(self.fontSize)
        self.destino = dependenciaRadioButtons(True)
        self.idioma = idiomaRadioButtons(True)
        self.pais = cbo(self.fontSize,
            items=['', 'México', 'United States'])
        self.pais.currentIndexChanged.connect(self.populateEstados)

        self.estado = cbo(self.fontSize)
        self.estado.currentIndexChanged.connect(self.populateCiudades)
        self.ciudad = cbo(self.fontSize)
        self.ciudad.currentIndexChanged.connect(self.populateOrigen)
        self.origen = cbo(self.fontSize)
        self.solicitante = lineEdit(self.fontSize)
        self.email = lineEdit(self.fontSize)
        self.telPais = cbo(self.fontSize,
            items=['', '+52','+1'])
        self.telNo = lineEditPhone(self.fontSize)
        self.notas = textEdit(self.fontSize)
        self.notas.setMinimumHeight(400)

        #o! ALL DB ITEMS THAT NEED TO BE POPULATED
        self.formItems = [self.id_, self.folio, self.titular, self.tipo, self.fecha,
            self.hojas, self.costo, self.destino, self.idioma, self.pais, self.estado,
            self.ciudad, self.origen, self.solicitante, self.email, self.telPais, self.telNo, self.notas]
        
        self.layoutForm.addRow(labelWidget('Id:', self.fontSize), self.id_)
        self.layoutForm.addRow(labelWidget('Folio:', self.fontSize), self.folio)
        self.layoutForm.addRow(labelWidget('Titular:', self.fontSize), self.titular)
        self.layoutForm.addRow(self.tipo)
        self.layoutForm.addRow(labelWidget('Fecha:', self.fontSize), self.fecha)
        self.layoutForm.addRow(labelWidget('Hojas:', self.fontSize), self.hojas)
        self.layoutForm.addRow(labelWidget('Costo:', self.fontSize), self.costo)
        self.layoutForm.addRow(self.destino)
        self.layoutForm.addRow(self.idioma)
        self.layoutForm.addRow(labelWidget('ORIGEN DEL DOCUMENTO:', 14,True,align="center"))
        self.layoutForm.addRow(labelWidget('Pais:', self.fontSize),self.pais)
        self.layoutForm.addRow(labelWidget('Estado:', self.fontSize),self.estado)
        self.layoutForm.addRow(labelWidget('Ciudad:', self.fontSize), self.ciudad)
        self.layoutForm.addRow(labelWidget('Origen:', self.fontSize), self.origen)
        self.layoutForm.addRow(labelWidget('DATOS DEL SOLICITANTE:', 14,True,align="center"))

        self.layoutForm.addRow(labelWidget('Solicitante:', self.fontSize), self.solicitante)
        self.layoutForm.addRow(labelWidget('Email:', self.fontSize), self.email)
        self.layoutForm.addRow(labelWidget('Tel pais:', self.fontSize), self.telPais)
        self.layoutForm.addRow(labelWidget('Telefono:', self.fontSize), self.telNo)
        self.layoutForm.addRow(labelWidget('Notas:', 14,True,align="center"))
        self.layoutForm.addRow(self.notas)
        self.layoutFormBox.setMinimumWidth(500)

    def setConnections(self):
        self.id_.textChanged.connect(lambda: self.formDirty(0,self.id_.getInfo()))
        self.folio.textChanged.connect(lambda: self.formDirty(1,self.folio.getInfo()))
        self.titular.textChanged.connect(lambda: self.formDirty(2,self.titular.getInfo()))
        for i in self.tipo.itemsList:
            i.toggled.connect(lambda: self.formDirty(3,self.tipo.getInfo()))
        self.fecha.dateEdit.dateChanged.connect(lambda: self.formDirty(4,self.fecha.getInfo()))
        self.hojas.valueChanged.connect(lambda: self.formDirty(5,self.hojas.getInfo()))
        self.costo.textChanged.connect(lambda: self.formDirty(6,self.costo.getInfo()))
        for i in self.destino.itemsList:
            i.toggled.connect(lambda: self.formDirty(7,self.destino.getInfo()))
        for i in self.idioma.itemsList:
            i.toggled.connect(lambda: self.formDirty(8,self.idioma.getInfo()))

        
        self.pais.currentTextChanged.connect(lambda: self.formDirty(9,self.pais.getInfo()))
        self.estado.currentTextChanged.connect(lambda: self.formDirty(10,self.estado.getInfo()))
        self.ciudad.currentTextChanged.connect(lambda: self.formDirty(11,self.ciudad.getInfo()))
        self.origen.currentTextChanged.connect(lambda: self.formDirty(12,self.origen.getInfo()))
        self.solicitante.textChanged.connect(lambda: self.formDirty(13,self.solicitante.getInfo()))
        self.email.textChanged.connect(lambda: self.formDirty(14,self.email.getInfo()))
        self.telPais.currentTextChanged.connect(lambda: self.formDirty(15,self.telPais.getInfo()))
        self.telNo.textChanged.connect(lambda: self.formDirty(16,self.telNo.getInfo()))
        self.notas.textChanged.connect(lambda: self.formDirty(17,self.notas.getInfo()))

    def populatePaisesFilter(self):
        a = '''--sql'''
        sql = '''
            SELECT DISTINCT pais FROM traducciones;
        '''
        paises = self.db.get_records_clearNull(sql)
        paises = list(map(lambda x: x[0], paises))
        paises.sort()
        self.paisFilter.insertNewItems(paises)

    def populateEstadosFilter(self):
        a = '''--sql'''
        sql = '''
            SELECT DISTINCT estado FROM traducciones
            WHERE pais LIKE %s;
        '''
        pais = self.paisFilter.getInfo()
        if not pais: pais = '%'

        estados = self.db.get_records_clearNull(sql, (pais,))
        estados = list(map(lambda x: x[0], estados))
        estados.append('')
        estados.sort()
        estados = set(estados)
        self.estadoFilter.insertNewItems(estados)

    def populateCiudadesFilter(self):
        a = '''--sql'''
        sql = '''
            SELECT DISTINCT ciudad FROM traducciones
            WHERE pais LIKE %s
            AND estado LIKE %s;
        '''
        pais = self.paisFilter.getInfo()
        if not pais: pais = '%'
        estado = self.estadoFilter.getInfo()
        if not estado: estado = '%'

        ciudades = self.db.get_records_clearNull(sql, (pais,estado))
        ciudades = list(map(lambda x: x[0], ciudades))
        ciudades.append('')
        ciudades.sort()
        ciudades = set(ciudades)
        self.ciudadFilter.insertNewItems(ciudades)

    def configure_list(self):
        self.tipoFilter = cboFilterGroup(self.fontSize,
            items=['','Nacimiento', 'Defuncion', 'Antecedentes', 'Divorcio', 'Identificacion', 'Matrimonio',
            'Poder', 'Solteria', 'Titulo', 'Otro'])
        self.list.layoutFilter.insertRow(0, labelWidget('Tipo:', self.filterSize), self.tipoFilter)
        
        self.ciudadFilter = cboFilterGroup(self.fontSize)
        # self.ciudadFilter.cbo.currentIndexChanged.connect(self.requery)
        self.list.layoutFilter.insertRow(0, labelWidget('Ciudad:', self.filterSize), self.ciudadFilter)

        self.estadoFilter = cboFilterGroup(self.fontSize)
        self.estadoFilter.cbo.currentIndexChanged.connect(self.estadoFilterApply)
        self.list.layoutFilter.insertRow(0, labelWidget('Estado:', self.filterSize), self.estadoFilter)
        
        self.paisFilter = cboFilterGroup(self.fontSize)
        self.paisFilter.cbo.currentIndexChanged.connect(self.paisFilterApply)
        self.list.layoutFilter.insertRow(0, labelWidget('Pais:', self.filterSize), self.paisFilter)

        self.yearFilter = cboFilterGroup(self.fontSize)
        self.yearFilter.insertNewItems(['','2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015'])
        self.list.layoutFilter.insertRow(0, labelWidget('Año:', self.filterSize), self.yearFilter)

        

        

        self.populatePaisesFilter()
        self.populateEstadosFilter()
        self.populateCiudadesFilter()

    def setFilesFolder(self):
        yearVar = self.fecha.dateEdit.date()
        yearVar = str(yearVar.year())
        folioVar = self.folio.text()
        tipoVar = self.tipo.getInfo()
        stateVar = self.estado.currentText()

        if yearVar and folioVar and tipoVar and stateVar:
            folderVar = f'{self.filesFolder.root}\{yearVar}_{folioVar}_{stateVar}_{tipoVar}'
            # fileVar = self.filesFolder.txtFilePath.text()
            folder = pathlib.Path(folderVar)
            if not folder.exists():
                os.mkdir(folderVar)
                self.filesFolder.txtFilePath.setText('folderVar')#sets an arbitrary value to refresh
            
            self.filesFolder.txtFilePath.setText(folderVar)
        else:
            self.filesFolder.txtFilePath.setText(self.filesFolder.root)

   
    def removeAllFilters(self):
        if self.paisFilter.getInfo():
            self.paisFilter.reSet()
        if self.estadoFilter.getInfo():
            self.estadoFilter.reSet()
        if self.ciudadFilter.getInfo():
            self.ciudadFilter.reSet()
        if self.tipoFilter.getInfo():
            self.tipoFilter.reSet()
        if self.list.filtros.txt.text():
            self.list.filtros.txt.reSet()

        self.requery()

    def paisFilterApply(self):
        self.populateEstadosFilter()
        # self.requery()

    def estadoFilterApply(self):
        self.populateCiudadesFilter()
        # self.requery()

    def btn_nuevo_pressed(self):
        super().btn_nuevo_pressed()
        date = datetime.now()
        year = date.year
        fecha = date.date()
        a = '''--sql'''
        sql = f'''
        SELECT MAX(folio) FROM traducciones
        WHERE YEAR(fecha) = {year};
        '''
        folio = self.db.get_records(sql)
        try:
            folio = int(folio[0][0])+1
        except:
            folio = 1

        a = '''--sql'''
        sql = f'''
        INSERT INTO traducciones (folio, fecha) VALUES ({folio}, '{fecha}');
        '''
        self.db.run_sql_commit(sql)
        a = '''--sql'''
        sql = f'''
        SELECT LAST_INSERT_ID();
        '''
        tradId = self.db.get_records(sql)
        tradId = tradId[0][0]
        self.requery()
        self.list.selectFirstItem()

    def getListInfo(self):
        record = super().getListInfo()
        fecha = self.fecha.dateEdit.date()
        year = fecha.year()
        folio = self.folio.getInfo()
        folio = str(folio).zfill(4)
        folioVar = f'{folio}/{str(year)}'
        record.insert(2, folioVar)
        return record

    def configureFormsFolder(self):
        self.btnForms = buttonWidget('Formatos', 'h1', constants.iconFolder)
        self.btnForms.pressed.connect(self.openFormsFolder)
        self.titleLayout.insertWidget(4, self.btnForms)

    def openFormsFolder(self):
        folder = f'{constants.oneDrive}\Despacho\Traducciones\Formatos'
        os.startfile(folder)
        


        




if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())