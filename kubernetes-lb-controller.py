# kubernetes-lb-controller - Main Controller Module
# This is where we instantiate everything.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

import sys
from helpers import globalholders
from helpers import database
from helpers import logutil
from helpers import kubeclient
from helpers import events

# Main :-)
def main():

    # Initiate the Database Connection
    if(database.connectDB() is False):
        logutil.printMessage("Error creating in-memory database")
        sys.exit(1)

    # Create our "in-memory" Route Table
    if(database.createDB() is False):
        logutil.printMessage("Error creating in-memory route table")
        sys.exit(1)

    # Load the IPs into the Route Table
    if(database.loadIPList() is False):
        logutil.printMessage("Error loading IPs into route table")
        sys.exit(1)

    # Load Kubernetes API Configuration
    if(kubeclient.loadConfig() is False):
        logutil.printMessage("Error loading Kubernetes Config")
        sys.exit(1)

    # Create Kubernetes API Connection
    if(kubeclient.connectApi() is False):
        logutil.printMessage("Error connecting to Kubernetes API")
        sys.exit(1)
        
    # Print the first route table to the file
    if(database.readDB() is not False):
        logutil.printRoutes(database.readDB())

    # Launch our Event Monitor/Handler
    logutil.printMessage("Starting the event handler.")
    events.launchHandler()
    logutil.printMessage("Event handler terminated.")
    sys.exit(1)

if __name__ == '__main__':
    main()
