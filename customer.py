#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.lib.agw.pycollapsiblepane
import tools

class CustomerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

    def getLabels(self):
        labels = []
        labels.append("Numero tessera:")
        labels.append("Nome:")
        labels.append("Cognome:")
        labels.append("Data di nascita:")
        labels.append("Comune di nascita:")
        labels.append("Provincia di nascita:")
        labels.append("Indirizzo:")
        labels.append("Città di residenza:")
        labels.append("Provincia di residenza:")
        labels.append("Attività:")
        labels.append("Tipo di iscrizione:")
        labels.append("Anno di iscrizione:")
        labels.append("Telefono:")
        labels.append("Cellulare:")
        labels.append("E-mail:")
        labels.append("Scadenza certificato:")
        return labels
    
    def getData(self, cust_id):
        conn = tools.getConnection()
        data = conn.getCustomerById(cust_id) if cust_id is not None else None
        if data is None:
            return None
        input = []
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
            input.append(unicode(data[i+1]))
        return input

class InsertCustomerForm(CustomerPanel):
    def __init__(self, parent):
        CustomerPanel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # User data
        ins = self.getData(None)
        labels = self.getLabels()
        self.inputs = []

        # Personal info
        sb1 = wx.StaticBox(self, -1, "Dati anagrifici:")
        hbox11 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        hbox1.Add(hbox11, 2, wx.EXPAND)

        fgs11 = wx.FlexGridSizer(12, 4, 3, 4)
        for i in range(9) + [12, 13, 14]:
            fgs11.Add(wx.StaticText(self, -1, labels[i]))
            self.inputs[i] = wx.TextCtrl(self, -1)
            fgs11.Add(self.inputs[i], 0, wx.EXPAND)
        fgs11.AddGrowableCol(1,1)
        fgs11.AddGrowableCol(3,1)
        hbox11.Add(fgs11, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(hbox1, 0, wx.EXPAND | wx.ALL, 15)

        # Bindings
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def OnPaneChanged(self, event):
        self.GetSizer().Layout()
        #self.Fit()
        event.Skip()

class CustomerInfo(CustomerPanel):
    def __init__(self, parent, rows, cols, vgap, hgap, cust_id=None):
        CustomerPanel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # User data
        self.inputs = []
        data = self.getData(cust_id)
        labels = self.getLabels()

        # Personal info
        sb1 = wx.StaticBox(self, -1, "Dati anagrifici:")
        hbox11 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
        hbox1.Add(hbox11, 2, wx.EXPAND)

        fgs11 = wx.FlexGridSizer(12, 4, vgap, hgap)
        for i in range(9) + [12, 13, 14]:
            fgs11.Add(wx.StaticText(self, -1, labels[i]))
            if data is None:
                self.inputs[i] = wx.TextCtrl(self, -1)
            else:
                self.inputs[i] = wx.StaticText(self, -1, data[i])
            fgs11.Add(self.inputs[i], 0, wx.EXPAND)
        fgs11.AddGrowableCol(1,1)
        fgs11.AddGrowableCol(3,1)
        hbox11.Add(fgs11, 1, wx.ALL | wx.EXPAND, 5)

        # Membership information
        sb2 = wx.StaticBox(self, -1, "Dati sociali:")
        hbox12 = wx.StaticBoxSizer(sb2, wx.HORIZONTAL)
        hbox1.Add(hbox12, 1, wx.EXPAND)
        fgs12 = wx.FlexGridSizer(4, 2, vgap, hgap)
        for i in [9, 10, 11, 15]:
            fgs12.Add(wx.StaticText(labels[i]))
            if data is None:
                self.inputs[i] = wx.TextCtrl(self, -1)
            else:
                self.inputs[i] = wx.StaticText(self, -1, data[i])
            fgs12.Add(self.inputs[i], 0, wx.EXPAND)
        fgs12.AddGrowableCol(1,1)
        fgs12.AddGrowableCol(3,1)
        hbox12.Add(fgs12, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(hbox1, 0, wx.EXPAND | wx.ALL, 15)

        # Renewals
        if cust_id is not None:
            ren = wx.lib.agw.pycollapsiblepane.PyCollapsiblePane(self, -1,  "Storico rinnovi:", style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
            win = ren.GetPane()
            vbox1 = wx.BoxSizer(wx.VERTICAL)
            self.renewals = tools.AWListCtrl(win, -1, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
            self.renewals.InsertColumn(0, "Data", width=140)
            self.renewals.InsertColumn(1, "Anno", width=60)
            self.renewals.InsertColumn(2, "Tipo iscrizione", width=200)
            vbox1.Add(self.renewals, 0, wx.EXPAND | wx.GROW)
            win.SetSizer(vbox1)
            vbox1.SetSizeHints(win)

            vbox.Add(ren, 0, wx.ALL | wx.GROW, 15)

        # Activities
        if cust_id is not None:
            act = wx.lib.agw.pycollapsiblepane.PyCollapsiblePane(self, -1,  "Riepilogo attività:", style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
            win = act.GetPane()
            vbox1 = wx.BoxSizer(wx.VERTICAL)
            self.activities = tools.AWListCtrl(win, -1, style=wx.LC_REPORT | wx.LC_HRULES)
            self.activities.InsertColumn(0, "Data", width=140)
            self.activities.InsertColumn(1, "Attività", width=400)
            self.activities.InsertColumn(2, "Importo", wx.LIST_FORMAT_RIGHT, width=90)
            self.activities.InsertColumn(3, "Pagato", width=90)
            vbox1.Add(self.activities, 0, wx.EXPAND | wx.GROW)
            win.SetSizer(vbox1)
            vbox1.SetSizeHints(win)

            vbox.Add(act, 0, wx.ALL | wx.GROW, 15)

        # Other Transactions
        if cust_id is not None:
            oth = wx.lib.agw.pycollapsiblepane.PyCollapsiblePane(self, -1,  "Prodotti acquistati:", style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
            win = oth.GetPane()
            vbox1 = wx.BoxSizer(wx.VERTICAL)
            self.others = tools.AWListCtrl(win, -1, style=wx.LC_REPORT | wx.LC_HRULES)
            self.others.InsertColumn(0, "Id", width=45)
            self.others.InsertColumn(1, "Servizio/Prodotto", width=400)
            self.others.InsertColumn(2, "Data", width=140)
            self.others.InsertColumn(3, "Importo", wx.LIST_FORMAT_RIGHT, width=90)
            self.others.InsertColumn(4, "Pagato", wx.LIST_FORMAT_RIGHT, width=90)
            self.others.InsertColumn(5, "Saldo", wx.LIST_FORMAT_RIGHT, width=90)
            vbox1.Add(self.others, 0, wx.EXPAND | wx.GROW)
            win.SetSizer(vbox1)
            vbox1.SetSizeHints(win)

            vbox.Add(oth, 0, wx.ALL | wx.GROW, 15)

        # Buttons
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        if cust_id is None:
            b = wx.Button(self, -1, 'Inserisci utente')
            b.Bind(wx.EVT_BUTTON, self.insertUser)
            buttonbox.Add(b, 1, wx.RIGHT, 5)
        else:
            buttonbox.Add(wx.Button(self, -1, 'Nuova transazione'), 1, wx.RIGHT, 5)
            buttonbox.Add(wx.Button(self, wx.ID_EDIT, 'Modifica utente'), 1, wx.RIGHT, 5)
        vbox.Add(buttonbox,0, wx.ALL, 15)

        # Bindings
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def OnPaneChanged(self, event):
        self.GetSizer().Layout()
        #self.Fit()
        event.Skip()


    def insertUser(self, event):
        data = [None]
        for i in self.inputs:
            if i.GetValue() == '':
                data.append(None)
            else:
                data.append(i.GetValue())
        conn = tools.getConnection()
        (i,s) = conn.insertCustomers([data])
        print "Inserted %d, skipped %d" % (i,s)
