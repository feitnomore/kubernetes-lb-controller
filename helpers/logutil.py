# logutil - Main Log Handler
# Helpers to print our status to the stdout, as well
# as saving the routing table on filesystem.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

import datetime
from prettytable import PrettyTable
from helpers import globalholders

# This is responsible for general message printing to stdout
def printMessage(message):
    # Getting the actual date/time
    my_time = datetime.datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
    # Print the log to the console
    print("[%s] %s" % (str(my_time), str(message)))

# This is responsible for printing the Events to stdout
def printEvent(event, ip, myaction, namespace, service, dst):
    # Getting the actual date/time
    my_time = datetime.datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
    # Print the log to the console
    print("[%s] %s %s %s namespace:%s service:%s destination:%s" % (str(my_time), str(event), str(ip), str(myaction), str(namespace), str(service), str(dst)))

# This is responsible for maintaining the local fs route table
# Route table on /routes
def printRoutes(allRoutes):
    # Getting the actual date/time
    my_time = datetime.datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
    # Opening/Creating the /routes file
    routeFile = open("/routes","w")
    # Creating a pretty table with the captions
    routeTable = PrettyTable(['IP','IN USE','NAMESPACE','SERVICE NAME','CLUSTER IP'])
    # Adding the routes to the table
    for thisRoute in allRoutes:
        routeTable.add_row(thisRoute)

    # Formatting our output
    strRouteTable = my_time + "\n" + str(routeTable) + "\n"
    # Writing table to the /route file
    routeFile.write(strRouteTable)

# This is our Exception Handler
def printException(e):
    # Opening our termination-log device
    terminationLog = open(globalholders.terminationDevice, "a")
    # Writing to the termination-log device
    terminationLog.write(e)