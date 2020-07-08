# events - Main Event Handler
# We monitor for events on Kubernetes. Here is the
# place were we are handling it.
# Events monitored are for Services, and work is done
# on service type LoadBalancer
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

from kubernetes import watch
from helpers import globalholders
from helpers import database
from helpers import services
from helpers import logutil

# This is the Handler
def launchHandler():
    w = watch.Watch()
    try: 
        while True:
            # Watching for event stream on Services
            for event in w.stream(globalholders.coreApi.list_service_for_all_namespaces):
                # A new service of type LoadBalancer was added
                if (event['type'] == "ADDED" and event['object'].spec.type == "LoadBalancer"):
                    my_service = event['object']
                    # Handle new service
                    services.added(my_service)
                    
                # A service of type LoadBalancer got modified
                elif(event['type'] == "MODIFIED" and event['object'].spec.type == "LoadBalancer"):
                    my_service = event['object']
                    # Handle updated service
                    services.modified(my_service)

                # A service of type LoadBalancer was deleted
                elif(event['type'] == "DELETED" and event['object'].spec.type == "LoadBalancer"):
                    my_service = event['object']
                    # Handle deleted service
                    services.deleted(my_service)

                # Get actual Route Table
                route_table = database.readDB()
                # Update Filesystem Route Table
                if(route_table is not False):
                    logutil.printRoutes(route_table)
                
    except Exception as e:
        logutil.printException(e)
        logutil.printMessage("Event Handler Exception: " + e)

