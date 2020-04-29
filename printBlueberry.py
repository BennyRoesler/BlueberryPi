import scanBlueberry as scanB
import time
import datetime

#Formatted printing for services.
def printServices(services):
    if(len(services) == 0):
        print("No results")
    else:
        host = "Host"
        name = "Name"
        manuf = scanB.getMan(host)
        description = "Description"
        provider = "Provider"
        protocol = "Protocol"
        port = "Port"
        service_classes = "Service Classes"
        profiles = "Profiles"
        print(f"|{host:^20}|{name:^30}|{manuf:^20}|{description:^20}|{provider:^20}|{protocol:^20}|{port:^20}")
        for match in services:
            host = "None" if match["host"] is None else match["host"]
            name = "None" if match["name"] is None else match["name"]
            manuf = scanB.getMan(host)
            description = "None" if match["description"] is None else match["description"]
            provider = "None" if match["provider"] is None else match["provider"]
            protocol = "None" if match["protocol"] is None else match["protocol"]
            port = "None" if match["port"] is None else match["port"]
            print(f"|{host:^20}|{name:^30}|{manuf:^20}|{description:^20}|{provider:^20}|{protocol:^20}|{port:^20}")

# Writes results to csv
def writeCSV(host, name, manuf, services, file):
    for match in services:
        serviceClass = "None" if match["service-classes"] is None else match["service-classes"]
        profiles = "None" if match["profiles"] is None else match["profiles"]
        servicesName = "None" if match["name"] is None else match["name"]
        description = "None" if match["description"] is None else match["description"]
        provider = "None" if match["provider"] is None else match["provider"]
        serviceID = "None" if match["service-id"] is None else match["service-id"]
        protocol = "None" if match["protocol"] is None else match["protocol"]
        port = "None" if match["port"] is None else match["port"]
        scanTime = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        file.writerow(
            [host, name, manuf, serviceClass, servicesName, profiles, description, provider, serviceID, protocol, port, scanTime])

def writeNoServicesCSV(host, name, manuf, file):
    file.writerow(
        [host, name, manuf, None, None, None, None, None, None, None, None, scanTime])
