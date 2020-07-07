# kubeclient - Main API Handler
# Handles the interaction with Kubernetes.
# Most of the changes and updates are here.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

import urllib3
from helpers import globalholders
from kubernetes import client
from kubernetes import config

# Loads configuration from Cluster
def loadConfig():
    try:
        # Disable SSL Warnings:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Load config from the Cluster (will use ServiceAccount)
        config.load_incluster_config()
        
        return True
        
    except Exception as e:
        return False

# Performs the API Connection
def connectApi():
    try:
        globalholders.coreApi = client.CoreV1Api()
        return True
    except Exception as e:
        return False

# Adds the IP to the Service
def serviceAddIP(service, ip):
    try:
        # Create an empty list for IPs
        ipList = list()
        if(ip is not None):
            # Append the IP to this list
            ipList.append(ip)
        # Update our local copy of the Service Descriptor
        service.spec.external_i_ps = ipList
        # Patch the cluster copy of the Service Descriptor
        globalholders.coreApi.patch_namespaced_service(service.metadata.name, service.metadata.namespace, service)
        return True
    except Exception as e:
        return False