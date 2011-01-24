import sqlite

conns = {}
def getConnection(name):
    if name not in conns:
        conns[name] = sqlite.Connection(name)
    return conns[name]

def closeConnection(name):
    if name not in conns:
        return;
    del conns[name]
