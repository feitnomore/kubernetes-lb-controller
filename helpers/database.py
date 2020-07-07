# database - Main Database Handler
# We use a "Ephemeral" SQLite in memory database to keep track of
# our routing table. Here is where we handle it.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

import os
import sqlite3
from helpers import globalholders

# Performs the DB Connection
def connectDB():
    try:
        globalholders.databaseConnection = sqlite3.connect(':memory:')
        return True
    except Exception as e:
        return False

# Creates our route table database
def createDB():
    try:
        cursor = globalholders.databaseConnection.cursor()
        cursor.execute('CREATE TABLE extips (ip VARCHAR(16) NOT NULL PRIMARY KEY, inuse CHAR(1) NOT NULL, namespace VARCHAR(64), service VARCHAR(64), dst VARCHAR(16));')
        globalholders.databaseConnection.commit()
        return True
    except Exception as e:
        return False

# Loads IPs from Configmap into the route table
def loadIPList():
    try:
        # List config files
        allNamespaces = os.listdir(globalholders.configPath)
        for namespace in allNamespaces:
            # Skipping internal files not related to our config
            if ".." not in namespace:
                namespacepath = globalholders.configPath + namespace
                with open(namespacepath) as ipList:
                    # Reading IPs from file
                    for ip in ipList:
                        cursor = globalholders.databaseConnection.cursor()
                        cursor.execute('INSERT INTO extips(ip,inuse,namespace) VALUES(?,?,?);' , (ip.strip(), 'n', namespace, ))
                        globalholders.databaseConnection.commit()
        return True
    except Exception as e:
        print(e)
        return False

# Read the route table
def readDB():
    try:
        cursor = globalholders.databaseConnection.cursor()
        cursor.execute('SELECT * FROM extips;')
        allRoutes = cursor.fetchall()
        return allRoutes
    except Exception as e:
        return False

# Get a free ip from the route table
def getIP(namespace, name):
    try:
        svc_line = ('n', namespace, name, )
        cursor = globalholders.databaseConnection.cursor()
        cursor.execute('SELECT ip FROM extips WHERE inuse=? AND namespace=? AND service=?;' , (svc_line))
        my_ip = cursor.fetchone()
        if(my_ip is None):
            svc_line = ('n', namespace, )
            cursor.execute('SELECT ip FROM extips WHERE inuse=? AND namespace=?;' , (svc_line))
            my_ip = cursor.fetchone()
            if(my_ip is None):
                return None
            else:
                return str(my_ip[0])
        else:
            return str(my_ip[0])
    except Exception as e:
        return None

# Marks IP as in use on route table
def consumeIP(ip, name, namespace, dst):
    try:
        cursor = globalholders.databaseConnection.cursor()
        flag = 'y'
        svc_line = (str(flag), str(namespace), str(name), str(dst), str(ip), )
        cursor.execute('UPDATE extips SET inuse=? , namespace=? , service=? , dst=? WHERE ip=?;', (svc_line))
        return True
    except Error as e:
        return False

# Check if IP is on our route table
def checkIP(ip):
    cursor = globalholders.databaseConnection.cursor()
    svc_ip = (ip, )
    cursor.execute('SELECT inuse FROM extips WHERE ip=?;', svc_ip)
    my_status = cursor.fetchone()
    if(my_status is None):
        return None
    else:
        return str(my_status[0])

# Check service for a IP in route table
def checkOwner(ip, name, namespace, dst):
    cursor = globalholders.databaseConnection.cursor()
    svc_ip = (ip, )
    cursor.execute('SELECT inuse, service, namespace, dst FROM extips WHERE ip=?', svc_ip)
    databaseEntry = cursor.fetchone()
    dbInuse, dbService, dbNamespace, dbDest = databaseEntry
    if(dbInuse == "y" and dbService == name and dbNamespace == namespace and dbDest == dst):
        return True
    else:
        return False

# Release IP on route table
def releaseIP(ip):
    try:
        cursor = globalholders.databaseConnection.cursor()
        flag = 'n'
        svc_line = (str(flag), None, str(ip), )
        cursor.execute('UPDATE extips SET inuse=? , dst=? WHERE ip=?;', (svc_line))
        return True
    except Exception as e:
        return False

# Get IP for a service on route table
def returnIP(name, namespace):
    cursor = globalholders.databaseConnection.cursor()
    svc_line = (namespace, name, )
    cursor.execute('SELECT ip FROM extips WHERE namespace=? AND service=?', svc_line)
    databaseEntry = cursor.fetchone()
    if(databaseEntry is None):
        return None
    else:
        svc_ip = databaseEntry[0]
        return str(svc_ip)
        
