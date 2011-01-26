import sqlite

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
