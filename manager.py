#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import os
import sys
import datetime

import customer

customers = [
        ("Michele", "Munno", "Via L. Battiferri, 15", datetime.date(2010, 10, 10), 0.00),
        ("Alice", "Devecchi", "Via L. Battiferri, 15", datetime.date(2011, 10, 10), 0.00),
        ("Stéphane", "Bisinger", "Viale XXV Aprile, 19", datetime.date(2011, 11, 21), -30.00),
        ("Arnaldo", "Lomuti", "Via Fadèn Telcul, 24", datetime.date(2011, 10, 23), 50.00),
        ]
class AWListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, style):
        wx.ListCtrl.__init__(self, parent, id, style=style)
        ListCtrlAutoWidthMixin.__init__(self)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,500))
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
        self.panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        sb = wx.SearchCtrl(self.panel, -1)
        sb.Bind(wx.EVT_TEXT, self.OnType)
        sb.SetDescriptiveText("Cerca cliente...")
        hbox1.Add(sb, 1)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1,10))
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #hbox2.Add(wx.StaticText(self.panel, -1, "Hilo"), 0)
        hbox2.Add(wx.StaticLine(self.panel), 1)
        vbox.Add(hbox2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.list = AWListCtrl(self.panel, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Nome", width=140)
        self.list.InsertColumn(1, "Cognome", width=140)
        self.list.InsertColumn(2, "Indirizzo", width=200)
        self.list.InsertColumn(3, "Cert.Med.", wx.LIST_FORMAT_RIGHT, width=90)
        self.list.InsertColumn(4, "Pagam.", wx.LIST_FORMAT_RIGHT, width=90)
        
        for c in customers:
            index = self.list.InsertStringItem(sys.maxint, c[0])
            self.list.SetStringItem(index, 1, c[1])
            self.list.SetStringItem(index, 2, c[2])
            self.list.SetStringItem(index, 3, str(c[3]))
            self.list.SetStringItem(index, 4, str(c[4]))
            if c[4] < 0 or c[3] <= datetime.date.today():
                self.list.SetItemTextColour(index, "red")
            if c[4] > 0:
                self.list.SetItemTextColour(index, "green")

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
        pass

    def OpenUser(self, event):
        d = wx.MessageDialog(self, self.list.GetItem(self.list.GetFocusedItem(), 1).GetText() + " Yeah", "Ducato Nuoto Manager", wx.OK)
        d.ShowModal()
        d.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Ducato Nuoto Manager")
app.MainLoop()
