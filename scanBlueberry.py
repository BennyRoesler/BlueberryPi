import bluetooth  # pip install pybluez
import pandas as pd
import printBlueberry as printB
import csv
import prettytable
import signal
import time
import datetime

#standard all scan, no writing to CSV
def scanAll(timeoutseconds=10):
    nearby_devices = bluetooth.discover_devices(duration=timeoutseconds, lookup_names=True)
    return nearby_devices


# Scan all available Bluetooth connections for all available services
def scanAllServices():
    results = bluetooth.find_service(name=None, uuid=None, address=None)

    if len(results) == 0:
        print("No devices found", flush=True)
        return

    printB.printServices(results)

# Scan services for singular macAddr
def scanOneService(addr, csvlocation="/tmp/Blueberry-DiscoveredDevices.csv"):

    print(f'Scanning for {addr} in the area')

    results = bluetooth.find_service(name=None, uuid=None, address=addr)

    print("Scan complete")
    if len(results) == 0:
        print(f'Unable to find "{addr}" for scan of services', flush=True)
        exit(1)

    CSVfile = open(csvlocation, 'w+')
    file = csv.writer(CSVfile)
    
    """ Writes to CSV """
    for i in results:
        host = i['host']
        name = i['name']
        manuf = getMan(host)
        serviceClass = i["service-classes"]
        profiles = i["profiles"]
        description = i['description']
        provider = i['provider']
        serviceID = i['service-id']
        protocol = i['protocol']
        port = i['port']
        file.writerow(
            [host, name, manuf, serviceClass, profiles, description, provider, serviceID, protocol, port])
    print('Raw CSV is located: ', csvlocation, flush=True)

    return results


# Scan services of all available bluetooth devices in range based on uuid value.
def scanUUIDService(uuidVal):
    service_matches = bluetooth.find_service(uuid=uuidVal, bdaddr=addr)

    if len(service_matches == 0):
        print(f'No services matching {uuidVal} found.', flush=True)
    else:
        printB.printServices(service_matches)


# Scan services of all available bluetooth devices in range based on name.
def scanNameService(nameVal):
    service_matches = bluetooth.find_service(name=nameVal, bdaddr=addr)

    if len(service_matches == 0):
        print(f'No services matching {nameVal} found.', flush=True)
    else:
        printB.printServices(service_matches)


# Compare given macAddr with current IEEE assignments
def getMan(macAddr):
    tempAddr = macAddr.replace(':', '')
    file = pd.read_csv("manufacturerOUI.csv")
    df = file[['Assignment', 'Organization Name']]

    for index, data in df.iterrows():
        if tempAddr.upper().startswith(data['Assignment']):
            return data['Organization Name']

# Standard continuous scan
def continuousScan(timeoutseconds=10, csvlocation="/tmp/Blueberry-DiscoveredDevices.csv"):
    ''' File I/O '''
    CSVfile = open(csvlocation, 'w+')
    file = csv.writer(CSVfile)

    ''' Init local var'''
    table = prettytable.PrettyTable(["MAC Address", "Device Name"])

    print(f'Continuous Scan will automatically end in {timeoutseconds} seconds', flush=True)

    results = scanAll(timeoutseconds)

    """ Writes to CSV """
    for resultAddr, resultName in results:
        host = resultAddr
        name = resultName
        manuf = getMan(host)
        print(f'FOUND: {host} - {name} - {manuf}', flush=True)
        services = scanOneService(host)

        if services is not None:
            table.add_row([host, name])
            printB.writeCSV(host, name, manuf, services, file)
        else:
            table.add_row([host, name])
            print(f"Service scan of {host} was unsuccessful, only writing basic data.", flush=True)

    print('Finishing Scan', flush=True)
    print(f"{len(results)} devices found", flush=True)
    print('Raw CSV is located: ', csvlocation, flush=True)
    CSVfile.close()
    print(table, flush=True)

# Repeatedly scans for devices
def asyncScan(timeoutseconds=10, csvlocation="/tmp/Blueberry-DiscoveredDevices.csv"):
    try:
        ''' File I/O'''
        CSVfile = open(csvlocation, 'w+')
        file = csv.writer(CSVfile)

        ''' Init local vars'''
        printed = []
        table = prettytable.PrettyTable(["MAC Address", "Device Name"])

        print(f'Asynchronous Scan will automatically end in {timeoutseconds} seconds', flush=True)
        print("Press CTRL+C (Keyboard Interrupt) to end scan early\n", flush=True)
        signal.signal(signal.SIGALRM, timeouthandler)  # raises a SIGALRM then calls function timeouthandler
        signal.setitimer(signal.ITIMER_REAL, timeoutseconds)  # second param is timer in seconds

        while True:
            devices_results = scanAll(timeoutseconds)
            service_results = bluetooth.find_service(name=None, uuid=None, address=None)

            """ Writes to CSV """
            for i in service_results:
                host = i['host']
                name = i['name']
                manuf = getMan(host)
                serviceClass = i["service-classes"]
                profiles = i["profiles"]
                description = i['description']
                provider = i['provider']
                serviceID = i['service-id']
                protocol = i['protocol']
                port = i['port']
                file.writerow(
                    [host, name, manuf, serviceClass, profiles, description, provider, serviceID, protocol, port])

            """ Prints newly found devices to console """
            for resultAddr, resultName in devices_results:
                if resultAddr not in printed:
                    host = resultAddr
                    name = resultName
                    manuf = getMan(host)
                    printed.append(host)
                    print(f'FOUND: {host} - {name} - {manuf}', flush=True)


    except KeyboardInterrupt:
        print('\nUser Interrupt Detected', flush=True)
        print('Finishing Scan', flush=True)
        print(f"{len(printed)} devices found", flush=True)
        print('Raw CSV is located: ', csvlocation, flush=True)
        CSVfile.close()
        print(table, flush=True)

    except TimeoutError:
        print('Time is up!', flush=True)
        print('Finishing Scan', flush=True)
        print(f"{len(printed)} devices found", flush=True)
        print('Raw CSV is located: ', csvlocation, flush=True)
        CSVfile.close()
        print(table, flush=True)


""" Used to send an TimeoutError exception to be caught by continousScan """
def timeouthandler(signum, frame):
    raise TimeoutError()
