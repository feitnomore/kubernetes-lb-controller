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
        # Creates "in-memory" database
        globalholders.databaseConnection = sqlite3.connect(':memory:')
        return True
    except Exception as e:
        return False

# Creates our route table database
def createDB():
    try:
        # Get a cursor on the database
        cursor = globalholders.databaseConnection.cursor()
        # Create the table that will hold our routes on the database
        cursor.execute('CREATE TABLE extips (ip VARCHAR(16) NOT NULL PRIMARY KEY, inuse CHAR(1) NOT NULL, namespace VARCHAR(64), service VARCHAR(64), dst VARCHAR(16));')
        # Commits the change to the database
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
                # Building the relative path for the namespace config file
                namespacepath = globalholders.configPath + namespace
                # Opening the config file
                with open(namespacepath) as ipList:
                    # Reading IPs from file
                    for ip in ipList:
                        cursor = globalholders.databaseConnection.cursor()
                        # Adding the IP to our table
                        cursor.execute('INSERT INTO extips(ip,inuse,namespace) VALUES(?,?,?);' , (ip.strip(), 'n', namespace, ))
                        globalholders.databaseConnection.commit()
        return True
    except Exception as e:
        return False

# Read the route table
def readDB():
    try:
        cursor = globalholders.databaseConnection.cursor()
        # Read everything from the database
        cursor.execute('SELECT * FROM extips;')
        allRoutes = cursor.fetchall()
        return allRoutes
    except Exception as e:
        return False

# Get a free ip from the route table
def getIP(namespace, name):
    try:
        # Will look for a free IP with the provided namespace and service name
        svc_line = ('n', namespace, name, )
        cursor = globalholders.databaseConnection.cursor()
        # Selects from the database IPs that are not in use and have the provided namespace and name
        cursor.execute('SELECT ip FROM extips WHERE inuse=? AND namespace=? AND service=?;' , (svc_line))
        my_ip = cursor.fetchone()
        # If IP was not found with provided namespace and name
        if(my_ip is None):
            # Will look for a free IP with the provided namespace
            svc_line = ('n', namespace, )
            # Selects from the database IPs that are not in use and have the provided namespace
            cursor.execute('SELECT ip FROM extips WHERE inuse=? AND namespace=?;' , (svc_line))
            my_ip = cursor.fetchone()
            if(my_ip is None):
                # No IPs found
                return None
            else:
                # Found IP for the provided Namespace
                return str(my_ip[0])
        else:
            # Found IP for the pair namespace/name
            return str(my_ip[0])
    except Exception as e:
        return None

# Marks IP as in use on route table
def consumeIP(ip, name, namespace, dst):
    try:
        cursor = globalholders.databaseConnection.cursor()
        flag = 'y'
        svc_line = (str(flag), str(namespace), str(name), str(dst), str(ip), )
        # Update the line flag to y for the provided parameters: IP, Name, Namespace, Destination
        cursor.execute('UPDATE extips SET inuse=? , namespace=? , service=? , dst=? WHERE ip=?;', (svc_line))
        return True
    except Error as e:
        return False

# Check if IP is on our route table
def checkIP(ip):
    cursor = globalholders.databaseConnection.cursor()
    svc_ip = (ip, )
    # Selects from database using provided IP as parameter
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
    # Selects the service line from our database
    cursor.execute('SELECT inuse, service, namespace, dst FROM extips WHERE ip=?', svc_ip)
    databaseEntry = cursor.fetchone()
    dbInuse, dbService, dbNamespace, dbDest = databaseEntry
    # Checks if database information matches provided parameters
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
        # Update the flag of the provided IP to not in use
        cursor.execute('UPDATE extips SET inuse=? , dst=? WHERE ip=?;', (svc_line))
        return True
    except Exception as e:
        return False

# Get IP for a service on route table
def returnIP(name, namespace):
    cursor = globalholders.databaseConnection.cursor()
    svc_line = (namespace, name, )
    # Will check the database for a IP with the provided Name and Namespace
    cursor.execute('SELECT ip FROM extips WHERE namespace=? AND service=?', svc_line)
    databaseEntry = cursor.fetchone()
    if(databaseEntry is None):
        return None
    else:
        svc_ip = databaseEntry[0]
        return str(svc_ip)
        
