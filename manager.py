#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.lib.agw.aui as aui
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin
import os
import sys
import datetime

import customer
import tools

customers = {
        1: ("Michele", "Munno", "Via L. Battiferri, 15", datetime.date(2010, 10, 10), 0.00),
        2: ("Alice", "Devecchi", "Via L. Battiferri, 15", datetime.date(2011, 10, 10), 0.00),
        3: (u'Stéphane', "Bisinger", "Viale XXV Aprile, 19", datetime.date(2011, 11, 21), -30.00),
        4: ("Arnaldo", "Lomuti", u'Via Fadèn Telcul, 24', datetime.date(2011, 10, 23), 50.00),
        5: ("Michael", "Micheli", "Via Trasanni, 45", datetime.date(2011, 9, 4), 10.00),
        6: ("Andrea", "Zanchetta", "Via Buonconte da Montefeltro, 11", datetime.date(2011, 9, 15), 1.00),
        }
customers2 = {
        1: ("ZMichele2", "Munno", "Via L. Battiferri, 15", datetime.date(2010, 10, 10), 0.00),
        2: ("Alice2", "Devecchi", "Via L. Battiferri, 15", datetime.date(2011, 10, 10), 0.00),
        3: (u'Stéphane2', "Bisinger", "Viale XXV Aprile, 19", datetime.date(2011, 11, 21), -30.00),
        4: ("Arnaldo2", "Lomuti", u'Via Fadèn Telcul, 24', datetime.date(2011, 10, 23), 50.00),
        }
class AWListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent, id, style):
        wx.ListCtrl.__init__(self, parent, id, style=style)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, 5)
        self.itemDataMap = customers

    def GetListCtrl(self):
        return self

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,750))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        self.Bind(wx.EVT_MENU, self.OnImport, filemenu.Append(wx.ID_OPEN, "&Importa", "Importa i dati da un foglio di calcolo Excel"))
        filemenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnExit, filemenu.Append(wx.ID_EXIT,"&Esci"," Termina l'esecuzione del programma"))

        # Setup customers menu
        customersmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.AddCustomer, customersmenu.Append(wx.ID_NEW, "&Nuovo cliente", "Aggiungi un nuovo cliente"))
        # Setup help menu
        helpmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnAbout, helpmenu.Append(wx.ID_ABOUT, "&Informazioni su..."," Informazioni sul programma"))

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(customersmenu,"&Clienti") # Adding the "customersmenu" to the MenuBar
        menuBar.Append(helpmenu,"&Aiuto") # Adding the "helpmenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Create the search box
        self.nb = aui.AuiNotebook(self, style=aui.AUI_NB_TOP
                | aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
                | aui.AUI_NB_MIDDLE_CLICK_CLOSE | aui.AUI_NB_DRAW_DND_TAB | aui.AUI_NB_HIDE_ON_SINGLE_TAB
                | aui.AUI_NB_WINDOWLIST_BUTTON)
        self.panel = wx.Panel(self.nb, -1)
        self.nb.AddPage(self.panel, "Gestione clienti")
        self.nb.SetArtProvider(aui.ChromeTabArt())

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sb = wx.SearchCtrl(self.panel, -1)
        self.sb.Bind(wx.EVT_TEXT, self.OnType)
        self.sb.SetDescriptiveText("Cerca cliente...")
        hbox1.Add(self.sb, 1)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1,10))
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticLine(self.panel), 1)
        vbox.Add(hbox2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.list = AWListCtrl(self.panel, -1, style=wx.LC_REPORT | wx.LC_HRULES)
        self.list.InsertColumn(0, "Nome", width=140)
        self.list.InsertColumn(1, "Cognome", width=140)
        self.list.InsertColumn(2, "Indirizzo", width=200)
        self.list.InsertColumn(3, "Cert.Med.", wx.LIST_FORMAT_RIGHT, width=90)
        self.list.InsertColumn(4, "Pagam.", wx.LIST_FORMAT_RIGHT, width=90)
        
        self.showCustomers(self.getProblematicCustomers())

        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenUser)
        vbox.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, 10)
        self.panel.SetSizer(vbox)

        self.Center()
        self.Show(True)

    def OnAbout(self, event):
        d = wx.MessageDialog(self, "Programma gestionale per piscine", "Ducato Nuoto Manager", wx.OK)
        d.ShowModal()
        d.Destroy()
    
    def OnExit(self, event):
        self.Close(True)

    def OnImport(self, event):
        self.dirname = ''
        d = wx.FileDialog(self, "Seleziona il file", self.dirname, "Foglio di calcolo Excel", "*.xls", wx.OPEN)
        if d.ShowModal() == wx.ID_OK:
            self.filename = d.GetFilename()
            self.dirname = d.GetDirectory()
            # Do something with the file
            a = wx.MessageDialog(self, os.path.join(self.dirname, self.filename), "File importato", wx.OK)
            a.ShowModal()
            a.Destroy()
        d.Destroy()

    def AddCustomer(self, event):
        try:
            # Is there a better way to do this??
            #self.ic.SetFocus()
            #self.ic.Raise()
            self.ic.Show(False)
            self.ic.Show(True)
        except AttributeError:
            self.ic = customer.InsertCustomer(self)

    def OnType(self, event):
        if len(self.sb.GetValue()) > 1:
            self.list.DeleteAllItems()
            self.showCustomers(self.findCustomers(self.sb.GetValue()))
        if len(self.sb.GetValue()) == 0:
            self.list.DeleteAllItems()
            self.showCustomers(self.getProblematicCustomers())

    def OpenUser(self, event):
        index = self.list.GetFocusedItem()
        up = wx.Panel(self.nb)
        self.nb.AddPage(up, self.list.GetItem(index, 0).GetText() + " " + self.list.GetItem(index, 1).GetText(), True)

    def getProblematicCustomers(self):
        return customers

    def findCustomers(self, hint):
        return customers2

    def showCustomers(self, dict):
        self.list.itemDataMap = dict
        item = dict.items()
        for key, data in item:
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetStringItem(index, 3, str(data[3]))
            self.list.SetStringItem(index, 4, str(data[4]))
            self.list.SetItemData(index, key)
            if data[3] <= datetime.date.today():
                self.list.SetItemBackgroundColour(index, "orange")
            if data[4] < 0:
                self.list.SetItemBackgroundColour(index, "red")
            if data[4] > 0:
                self.list.SetItemBackgroundColour(index, "green")


conn = tools.getConnection("dnmdb")
conn.createTables()
del conn
tools.closeConnection("dnmdb")
app = wx.App(False)
frame = MainWindow(None, "Ducato Nuoto Manager")
app.MainLoop()
