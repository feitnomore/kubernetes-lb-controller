# services - Main Service Handler
# Helpers to handle the service action intercepted
# by our Event Handler.
# We can either Add, modify or delete
# a given Service.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

from helpers import globalholders
from helpers import kubeclient
from helpers import database
from helpers import logutil


# Handles events of type "ADDED"
def added(service):
    # Service added without external_ip
    if(service.spec.external_i_ps is None):
        # Try to get a free IP from our route table
        ip = database.getIP(service.metadata.namespace, service.metadata.name)
        if(ip is not None):
            # Setting up returned IP
            if(kubeclient.serviceAddIP(service, ip) is True):
                # Added IP to the Service
                if(database.consumeIP(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) is True):
                    # Route table updated
                    logutil.printEvent("ADDED", ip, "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
                else:
                    # Failed updating route table
                    logutil.printEvent("ADDED", ip, "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # Failed adding IP to the Service
                logutil.printEvent("ADDED", ip, "FAILED_API", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        else:
            # There are no free IPs
            logutil.printEvent("ADDED", "XXX.XXX.XXX.XXX", "NOT_AVAILABLE", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
    # Service added with IP in it
    else:
        # Verify if IP is on route table and free
        ip_status = database.checkIP(service.spec.external_i_ps[0])
        if(ip_status == "n"):
            # IP is free, lets update our route table
            if(database.consumeIP(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) is True):
                # Route table updated
                logutil.printEvent("ADDED", service.spec.external_i_ps[0], "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # Failed updating the route table
                logutil.printEvent("ADDED", service.spec.external_i_ps[0], "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        elif(ip_status == "y"):
            # IP is not free
            if(database.checkOwner(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) == False):
                # This IP is in use by someone else, lets remove it from service
                if(kubeclient.serviceAddIP(service, None) is True):
                    # IP removed from Service
                    logutil.printEvent("ADDED", "XXX.XXX.XXX.XXX", "IN_USE", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
                else:
                    # Failed removing IP from Service
                    logutil.printEvent("ADDED", "XXX.XXX.XXX.XXX", "FAILED_API", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # This IP was already in use by me
                logutil.printEvent("ADDED", service.spec.external_i_ps[0], "NO_ACTION", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        else:
            # IP is not on our route table, lets ignore
            logutil.printEvent("ADDED", service.spec.external_i_ps[0], "IGNORED", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)

# Handles events of type "MODIFIED"
def modified(service):
    # Service Modified without external_ip
    if(service.spec.external_i_ps is None):
        # Checking if this service has a IP on our route table
        svc_ip = database.returnIP(service.metadata.name, service.metadata.namespace)
        if(svc_ip is not None):
            # The service already have a IP on our route table
            # We will update the service to use it
            ip = svc_ip
            if(kubeclient.serviceAddIP(service, ip) is True):
                # Added IP to Service
                if(database.consumeIP(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) is True):
                    # Route table updated
                    logutil.printEvent("MODIFIED", ip, "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
                else:
                    # Failed updating route table
                    logutil.printEvent("MODIFIED", ip, "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # Failed adding IP to the Service
                logutil.printEvent("MODIFIED", ip, "FAILED_API", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        else:
            # The service has no IP on our route table
            # Try to get a free IP from our route table
            ip = database.getIP(service.metadata.namespace, service.metadata.name)
            if(ip is not None):
                # Setting up returned IP
                if(kubeclient.serviceAddIP(service, ip) is True):
                    # Added IP to Service
                    if(database.consumeIP(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) is True):
                        # Route table updated
                        logutil.printEvent("MODIFIED", ip, "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
                    else:
                        # Failed updating route table
                        logutil.printEvent("MODIFIED", ip, "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
                else:
                    # Failed adding IP to the Service
                    logutil.printEvent("MODIFIED", ip, "FAILED_API", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # There are no free IPs
                logutil.printEvent("MODIFIED", "XXX.XXX.XXX.XXX", "NOT_AVAILABLE", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
    # Service Modified with external_ip
    else:
        # Verify if IP is on route table and free
        ip_status = database.checkIP(service.spec.external_i_ps[0])
        # Check if service had IP on Route Table
        ip_on_route_table = database.returnIP(service.metadata.name, service.metadata.namespace)
        if(ip_status == "n"):
            # IP is free, lets update route table
            if(database.consumeIP(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) is True):
                if(ip_on_route_table is not None):
                    database.releaseIP(ip_on_route_table)
                # Updated route table
                logutil.printEvent("MODIFIED", service.spec.external_i_ps[0], "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # Failed updating route table
                logutil.printEvent("MODIFIED", service.spec.external_i_ps[0], "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        elif(ip_status == "y"):
            # IP is not free
            if(database.checkOwner(service.spec.external_i_ps[0], service.metadata.name, service.metadata.namespace, service.spec.cluster_ip) == False):
                # This IP is in use by someone else, lets remove it from service
                if(kubeclient.serviceAddIP(service, None) is True):
                    # IP removed from Service
                    logutil.printEvent("MODIFIED", "XXX.XXX.XXX.XXX", "NOT_AVAILABLE", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
                else:
                    # Failed removing IP from Service
                    logutil.printEvent("MODIFIED", "XXX.XXX.XXX.XXX", "FAILED_API", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # This IP was already in use by me
                logutil.printEvent("MODIFIED", service.spec.external_i_ps[0], "IGNORED", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        else:
            # Verify old IP on database and cleanup
            if(ip_on_route_table is not None):
                database.releaseIP(ip_on_route_table)
                logutil.printEvent("MODIFIED", ip_on_route_table, "IGNORED", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # IP is not on our route table, lets ignore
                logutil.printEvent("MODIFIED", service.spec.external_i_ps[0], "IGNORED", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)

# Handles events of type "DELETED"
def deleted(service):
    # Verify if service has IP
    if(service.spec.external_i_ps is not None):
        # Verify if IP is on our route table
        svc_ip = database.checkIP(service.spec.external_i_ps[0])
        # IP is on route table, lets update the table
        if(database.releaseIP(service.spec.external_i_ps[0]) is True):
            # Route table updated
            logutil.printEvent("DELETED", service.spec.external_i_ps[0], "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        else:
            # Failed updating route table
            logutil.printEvent("DELETED", service.spec.external_i_ps[0], "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
    else:
        # Looking up service IP by name
        svc_ip = database.returnIP(service.metadata.name, service.metadata.namespace)
        if(svc_ip is not None):
            # Found and IP for this service on the route table
            if(database.releaseIP(svc_ip) is True):
                # Route table updated
                logutil.printEvent("DELETED", svc_ip, "OK", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
            else:
                # Failed updating route table
                logutil.printEvent("DELETED", svc_ip, "FAILED_DB", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
        else:
            # IP is not on route table, lets ignore it
            logutil.printEvent("DELETED", "XXX.XXX.XXX.XXX", "IGNORED", service.metadata.namespace, service.metadata.name, service.spec.cluster_ip)
