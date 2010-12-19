#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

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
