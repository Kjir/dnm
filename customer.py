#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import tools

class InsertCustomer(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Inserisci cliente", size=(500,300))
        self.CreateStatusBar()
        filemenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnExit, filemenu.Append(wx.ID_CLOSE,"&Chiudi"," Chiudi la finestra"))
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)

        self.CenterOnParent()
        self.Show(True)

    def OnExit(self, event):
        self.Close(True)

class CustomerForm(wx.Panel):
    def __init__(self, parent, rows, cols, vgap, hgap, cust_id=None):
        #wx.Frame.__init__(self, parent, title="Inserisci cliente", size=(500,300))
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # User data
        conn = tools.getConnection()
        data = conn.getCustomerById(cust_id) if cust_id is not None else None
        input = []
        labels = []
        for i in range(16):
            #if i == 3:
            #    d = wx.DateTime()
            #    if data is None:
            #        input.append(wx.DatePickerCtrl(self, dt=d))
            #    elif d.ParseFormat(data[i+1], "%Y-%m-%d") is not None:
            #        print data[i+1]
            #        input.append(wx.DatePickerCtrl(self))
            #        input[i].SetValue(d)
            #    else:
            #        input.append(wx.TextCtrl(self, -1))

            #else:
                if data is not None:
                    input.append(wx.StaticText(self, -1, unicode(data[i+1])))
                else:
                    input.append(wx.TextCtrl(self, -1))

        labels.append(wx.StaticText(self, -1, "Numero tessera:"))
        labels.append(wx.StaticText(self, -1, "Nome:"))
        labels.append(wx.StaticText(self, -1, "Cognome:"))
        labels.append(wx.StaticText(self, -1, "Data di nascita:"))
        labels.append(wx.StaticText(self, -1, "Comune di nascita:"))
        labels.append(wx.StaticText(self, -1, "Provincia di nascita:"))
        labels.append(wx.StaticText(self, -1, "Indirizzo:"))
        labels.append(wx.StaticText(self, -1, "Città di residenza:"))
        labels.append(wx.StaticText(self, -1, "Provincia di residenza:"))
        labels.append(wx.StaticText(self, -1, "Attività:"))
        labels.append(wx.StaticText(self, -1, "Tipo di iscrizione:"))
        labels.append(wx.StaticText(self, -1, "Anno di iscrizione:"))
        labels.append(wx.StaticText(self, -1, "Telefono:"))
        labels.append(wx.StaticText(self, -1, "Cellulare:"))
        labels.append(wx.StaticText(self, -1, "E-mail:"))
        labels.append(wx.StaticText(self, -1, "Data di scadenza certificato:"))

        # Personal info
        sb1 = wx.StaticBox(self, -1, "Dati anagrifici:")
        hbox11 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        hbox1.Add(hbox11, 2, wx.EXPAND)

        fgs11 = wx.FlexGridSizer(12, 4, vgap, hgap)
        for i in range(9) + [12, 13, 14]:
            fgs11.Add(labels[i])
            fgs11.Add(input[i], 0, wx.EXPAND)
        fgs11.AddGrowableCol(1,1)
        fgs11.AddGrowableCol(3,1)
        hbox11.Add(fgs11, 1, wx.ALL | wx.EXPAND, 5)

        # Membership information
        sb2 = wx.StaticBox(self, -1, "Dati sociali:")
        hbox12 = wx.StaticBoxSizer(sb2, wx.HORIZONTAL)
        hbox1.Add(hbox12, 1, wx.EXPAND)
        fgs12 = wx.FlexGridSizer(4, 2, vgap, hgap)
        for i in [9, 10, 11, 15]:
            fgs12.Add(labels[i])
            fgs12.Add(input[i], 0, wx.EXPAND)
        fgs12.AddGrowableCol(1,1)
        fgs12.AddGrowableCol(3,1)
        hbox12.Add(fgs12, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(hbox1, 0, wx.EXPAND | wx.ALL, 15)

        # Transactions
        sb = wx.StaticBox(self, -1,  "Transazioni:")
        vbox1 = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.list = tools.AWListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_HRULES)
        self.list.InsertColumn(0, "Id", width=45)
        self.list.InsertColumn(1, "Servizio/Prodotto", width=400)
        self.list.InsertColumn(2, "Data", width=140)
        self.list.InsertColumn(3, "Importo", wx.LIST_FORMAT_RIGHT, width=90)
        self.list.InsertColumn(4, "Pagato", wx.LIST_FORMAT_RIGHT, width=90)
        self.list.InsertColumn(5, "Saldo", wx.LIST_FORMAT_RIGHT, width=90)
        vbox1.Add(self.list, 0, wx.EXPAND)

        vbox.Add(vbox1, 0, wx.EXPAND | wx.ALL, 15)

        # Buttons
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        buttonbox.Add(wx.Button(self, -1, 'Nuova transazione'), 1, wx.RIGHT, 5)
        buttonbox.Add(wx.Button(self, wx.ID_EDIT, 'Modifica utente'), 1, wx.RIGHT, 5)
        vbox.Add(buttonbox,0, wx.ALL, 15)
