import sqlite
from wx import ListCtrl
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

default_connection_name = "dnmdb"
conns = {}
def setDefaultConnectionName(name):
    default_connection_name = name

def getConnection(name=None):
    if name is None:
        name = default_connection_name
    if name not in conns:
        conns[name] = sqlite.Connection(name)
    return conns[name]

def closeConnection(name=None):
    if name is None:
        name = default_connection_name
    if name not in conns:
        return;
    del conns[name]

class AWListCtrl(ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent, id, style, sort=5):
        ListCtrl.__init__(self, parent, id, style=style)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, sort)

    def GetListCtrl(self):
        return self

