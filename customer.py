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
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)
        fgs = wx.FlexGridSizer(rows, cols, vgap, hgap)

        conn = tools.getConnection()
        data = conn.getCustomerById(cust_id) if cust_id is not None else None
        input = []
        labels = []
        for i in range(16):
            if i == 3:
                d = wx.DateTime()
                if data is None:
                    input.append(wx.DatePickerCtrl(self))
                elif d.ParseFormat(data[i+1], "%Y-%m-%d"):
                    print d.ParseFormat(data[i+1], "%Y-%m-%d")
                    print data[i+1]
                    input.append(wx.DatePickerCtrl(self))
                    d = wx.DateTime()
                    input[i].SetValue(d)
                else:
                    input.append(wx.TextCtrl(self, -1))

            else:
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
        for i in range(16):
            fgs.Add(labels[i])
            fgs.Add(input[i], wx.EXPAND)

        fgs.AddGrowableCol(1,1)
        fgs.AddGrowableCol(3,1)
        hbox.Add(fgs, 1, wx.ALL | wx.EXPAND, 15)
