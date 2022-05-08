#!/usr/bin/python3
 
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc 
from PyQt6 import QtGui as qtg 
from globalElements.treeview import treeviewSearchBox
from globalElements.widgets import labelWidget
from decimal import *
import re
import locale
locale.setlocale(locale.LC_ALL,"")

class main(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.treeview = treeviewSearchBox()
        self.sortColumn = 6
        self.sortOrder = qtc.Qt.SortOrder.DescendingOrder
        self.setCentralWidget(self.treeview)
        #G! CONFIGURE TOTAL 
        self.avd = labelWidget('', 13)
        self.dnp = labelWidget('', 13)
        self.calvillo = labelWidget('', 13)

        self.totals = labelWidget('', 16, True)
        self.totals.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
        self.treeview.layoutDetails.addRow(labelWidget("AVD:", 13), self.avd)
        self.treeview.layoutDetails.addRow(labelWidget("DNP:", 13), self.dnp)
        self.treeview.layoutDetails.addRow(labelWidget("Calvillo:", 13), self.calvillo)
        self.treeview.layoutDetails.addRow(labelWidget("Total:", 14, True), self.totals)
        #G! connections for totals
        # self.treeview.proxyModel.dataChanged.connect(self.setTotals)
        self.treeview.proxyModel.rowsInserted.connect(self.setTotals)
        self.treeview.proxyModel.rowsRemoved.connect(self.setTotals)
        
        
    def setTotals(self):
        amounts = self.treeview.getColumnValues((10,2))
        total = Decimal('0.00') 
        avd = Decimal('0.00') 
        dnp = Decimal('0.00') 
        calvillo = Decimal('0.00') 
        for i in amounts:
            loadtotal  = Decimal(re.sub(r"[^\d.]","", i[0]))
            carrier = i[1]
            if carrier == "DNP FREIGHT LLC":
                carrierPay  = loadtotal*Decimal(.87)
                dnp += carrierPay
                avd += loadtotal - carrierPay
            elif carrier == "T M CALVILLO TRANSPORT":
                carrierPay = loadtotal*Decimal(.93)
                calvillo += carrierPay
                avd += loadtotal - carrierPay
            elif carrier == "AVD TRUCKING LLC":
                avd += loadtotal


        total = avd + calvillo + dnp    
        total = Decimal(total.quantize(Decimal(".01")))
        total = locale.currency(float(total), grouping=True)
        self.totals.setText(str(total))

        avd = Decimal(avd.quantize(Decimal(".01")))
        avd = locale.currency(float(avd), grouping=True)
        self.avd.setText(str(avd))

        dnp = Decimal(dnp.quantize(Decimal(".01")))
        dnp = locale.currency(float(dnp), grouping=True)
        self.dnp.setText(str(dnp))

        calvillo = Decimal(calvillo.quantize(Decimal(".01")))
        calvillo = locale.currency(float(calvillo), grouping=True)
        self.calvillo.setText(str(calvillo))


        # self.setHCarrierRate()

    def configureColumns(self):
        #o! list of columns index and their width to set on treeview
        columnsWidth = ((0,60),(6,100),(7,300), (10,100))
        self.treeview.setColumnsWith(columnsWidth)
          
        #o! list of columns index to be hidden
        #Show 0-id, 6-date, 7-Client, 10-rate, 
        columnsHidden = (1,2,3,4,5,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24)#13,14,15,16,17
        self.treeview.setHiddenColums(columnsHidden)
        self.treeview.search_afterUpdate(self.sortColumn, self.sortOrder)#o! VERIFY SORT COLUMN
        # self.treeview.proxyModel.insertColumn(11)
        
    # def setHCarrierRate(self):
    #     totalRows = self.treeview.proxyModel.rowCount()
    #     currentRow = 0
    #     avd = Decimal('0.00') 
    #     dnp = Decimal('0.00') 
    #     calvillo = Decimal('0.00') 
    #     while currentRow < totalRows:
    #         total = self.treeview.proxyModel.index(currentRow, 10).data()
    #         if total:
    #             total  = Decimal(total)#(re.sub(r"[^\d.]","", total))
    #             carrier = self.treeview.proxyModel.index(currentRow, 2).data()
    #             if carrier == "1":
    #                 dnp += total*Decimal(.87)
    #                 avd += total*Decimal(.13)
    #             elif carrier == "3":
    #                 calvillo += total*Decimal(.93)
    #                 avd += total*Decimal(.07)
    #             elif carrier == "2":
    #                 avd += total
    #         currentRow += 1
        
    #     avd = Decimal(avd.quantize(Decimal(".01")))
    #     avd = locale.currency(float(avd), grouping=True)
    #     # self.totals.setText(str(total))
    #     dnp = Decimal(dnp.quantize(Decimal(".01")))
    #     dnp = locale.currency(float(dnp), grouping=True)

    #     calvillo = Decimal(calvillo.quantize(Decimal(".01")))
    #     calvillo = locale.currency(float(calvillo), grouping=True)

    #     # print(dnp, "--", avd,'--', calvillo)
    #     return dnp, avd, calvillo
