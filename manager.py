#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.agw.aui as aui
import os
import sys
import datetime

import customer
import tools

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

        self.list = tools.AWListCtrl(self.panel, -1, style=wx.LC_REPORT | wx.LC_HRULES)
        self.list.InsertColumn(0, "Id", width=45)
        self.list.InsertColumn(1, "Nome", width=140)
        self.list.InsertColumn(2, "Cognome", width=140)
        self.list.InsertColumn(3, "Indirizzo", width=200)
        self.list.InsertColumn(4, "Cert.Med.", wx.LIST_FORMAT_RIGHT, width=90)
        self.list.InsertColumn(5, "Pagam.", wx.LIST_FORMAT_RIGHT, width=90)
        
        self.showCustomers(self.getProblematicCustomers())

        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OpenUser)
        vbox.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, 10)
        self.panel.SetSizer(vbox)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChange)

        # Insert customer page for notebook
        self.ins_cust = None

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
            import excel
            data = excel.importfile(os.path.join(self.dirname, self.filename))
            conn = tools.getConnection()
            (inserted, skipped) = conn.insertCustomers(data)
            del conn
            a = wx.MessageDialog(self, "Importati %d utenti da %s, %d ignorati." % (inserted, self.filename, skipped), "File importato", wx.OK)
            a.ShowModal()
            a.Destroy()
            self.OnType(None)
        d.Destroy()

    def AddCustomer(self, event):
        if self.ins_cust is not None:
            idx = self.nb.GetPageIndex(self.ins_cust)
            if idx <> -1:
                self.nb.SetSelection(idx)
                return
        self.ins_cust = customer.InsertCustomerForm(self.nb)
        self.nb.AddPage(self.ins_cust, "Nuovo cliente", True)

    def OnType(self, event):
        if len(self.sb.GetValue()) > 1:
            self.list.DeleteAllItems()
            self.showCustomers(self.findCustomers(self.sb.GetValue()))
        if len(self.sb.GetValue()) == 0:
            self.list.DeleteAllItems()
            self.showCustomers(self.getProblematicCustomers())

    def OnPaneChange(self, event):
        self.Fit()

    def OpenUser(self, event):
        index = self.list.GetFocusedItem()
        up = customer.CustomerInfo(self.nb, 8, 4, 3, 4, int(self.list.GetItem(index, 0).GetText()))
        self.nb.AddPage(up, self.list.GetItem(index, 1).GetText() + " " + self.list.GetItem(index, 2).GetText(), True)

    def getProblematicCustomers(self):
        conn = tools.getConnection()
        return conn.getProblematicCustomers()

    def findCustomers(self, hint):
        conn = tools.getConnection()
        return conn.findCustomer(hint)

    def showCustomers(self, dict):
        self.list.itemDataMap = dict
        item = dict.items()
        for key, data in item:
            index = self.list.InsertStringItem(sys.maxint, str(data[0]))
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetStringItem(index, 3, data[3])
            self.list.SetStringItem(index, 4, str(data[4]))
            self.list.SetStringItem(index, 5, str(data[5]))
            self.list.SetItemData(index, key)
            try:
                if data[4] is None or datetime.datetime.strptime(data[4], "%Y-%m-%d") <= datetime.datetime.today():
                    self.list.SetItemBackgroundColour(index, "orange")
            except ValueError, e:
                print e
            if data[5] < 0:
                self.list.SetItemBackgroundColour(index, "red")
            if data[5] > 0:
                self.list.SetItemBackgroundColour(index, "green")


tools.setDefaultConnectionName("dnmdb")
conn = tools.getConnection()
conn.createTables()
del conn
tools.closeConnection()
app = wx.App(False)
frame = MainWindow(None, "Ducato Nuoto Manager")
#import wx.lib.inspection
#wx.lib.inspection.InspectionTool().Show()
app.MainLoop()
