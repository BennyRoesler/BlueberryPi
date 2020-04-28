import bluetooth  # pip install pybluez
import pandas as pd
import printBlueberry as printB
import csv
import prettytable
import signal


# Scans all nearby bluetooth devices, return list of MACS and Device Names(if available). Devices must be in discoverable mode. Does not work with low power Bluetooth
def scanAll():
    # Standard ble check
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)

    print(f'Found {len(nearby_devices)} devices')

    for addr, name in nearby_devices:
        print(f'{addr}  -   {name}')


# Scan all available Bluetooth connections for all available services
def scanAllServices():
    results = bluetooth.find_service(name=None, uuid=None, address=None)

    if len(results) == 0:
        print("No devices found")
        return

    printB.printServices(results)


def scanOneService(addr):
    results = bluetooth.find_service(name=None, uuid=None, address=addr)

    if len(results) == 0:
        print(f'Unable to find "{addr}"')
        return

    printB.printServices(results)


# Scan services of all available bluetooth devices in range based on uuid value. Second arg for one device only
def scanUUIDService(uuidVal, addr=None):
    service_matches = bluetooth.find_service(uuid=uuidVal, bdaddr=addr)

    if len(service_matches == 0):
        print(f'No services matching {uuidVal} found.')
    else:
        printB.printServices(service_matches)


# Scan services of all available bluetooth devices in range based on name. Second arg for one device only
def scanNameService(nameVal, addr=None):
    service_matches = bluetooth.find_service(name=nameVal, bdaddr=addr)

    if len(service_matches == 0):
        print(f'No services matching {nameVal} found.')
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

# Repeatedly scans for devices
def continousScan(timeoutseconds=10, csvlocation="/tmp/Blueberry-DiscoveredDevices.csv"):
    try:
        ''' File I/O'''
        CSVfile = open(csvlocation, 'w+')
        file = csv.writer(CSVfile)

        ''' Init local vars'''
        printed = []
        table = prettytable.PrettyTable(["MAC Address", "Device Name"])

        print(f'Scan will automatically end in {timeoutseconds} seconds')
        print("Press CTRL+C (Keyboard Interrupt) to end scan early\n")
        signal.signal(signal.SIGALRM, timeouthandler)  # raises a SIGALRM then calls function timeouthandler
        signal.setitimer(signal.ITIMER_REAL, timeoutseconds)  # second param is timer in seconds

        while True:
            print("Iteration - Should be scanning for new BT devices - Delete this before turning it in")
            results = bluetooth.find_service(name=None, uuid=None, address=None)

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

            """ Prints newly found devices to console """
            for i in results:
                if i['host'] not in printed:
                    host = i['host']
                    name = i['name']
                    table.add_row([host, name])
                    print(f'Discovered:', host)
                    printed.append(host)


    except KeyboardInterrupt:
        print('\nUser Interrupt Detected')
        print('Finishing Scan')
        print(f"{len(printed)} devices found")
        print('Raw CSV is located: ', csvlocation)
        CSVfile.close()
        print(table)
        exit(1)

    except TimeoutError:
        print('Time is up!')
        print('Finishing Scan')
        print(f"{len(printed)} devices found")
        print('Raw CSV is located: ', csvlocation)
        CSVfile.close()
        print(table)
        exit(1)


""" Used to send an TimeoutError exception to be caught by continousScan """
def timeouthandler(signum, frame):
    raise TimeoutError()


continousScan(timeoutseconds=30)
