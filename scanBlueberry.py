import bluetooth
import pandas as pd
import printBlueberry as printB

#Scans all nearby bluetooth devices, return list of MACS and Device Names(if available). Devices must be in discoverable mode. Does not work with low power Bluetooth
def scanAll():
    #Standard ble check
    nearby_devices = bluetooth.discover_devices(duration = 10, lookup_names=True)

    print(f'found {len(nearby_devices)}')

    for addr, name in nearby_devices:
        print(f'{addr}  -   {name}')

#Scan all available Bluetooth connections for all available services
def scanAllServices():
    results = bluetooth.find_service(name = None, uuid = None, address = None)

    printB.printServices(results)

def scanOneService(addr):
    results = bluetooth.find_service(name = None, uuid = None, address = addr)

    printB.printServices(results)

#Scan services of all available bluetooth devices in range based on uuid value. Second arg for one device only
def scanUUIDService(uuidVal, addr = None):
    service_matches = bluetooth.find_service(uuid = uuidVal, bdaddr = addr)

    if len(service_matches == 0):
        printf(f'No services matching {uuidVal} found.')
    else:
        printB.printServices(service_matches)

#Scan services of all available bluetooth devices in range based on name. Second arg for one device only
def scanNameService(nameVal, addr = None):
    service_matches = bluetooth.find_service(name = nameVal, bdaddr = addr)

    if len(service_matches == 0):
        printf(f'No services matching {uuidVal} found.')
    else:
        printB.printServices(service_matches)

#Compare given macAddr with current IEEE assignments
def getMan(macAddr):
    tempAddr = macAddr.replace(':', '')
    file = pd.read_csv("manufacturerOUI.csv")
    df = file[['Assignment', 'Organization Name']]

    for index, data in df.iterrows():
        if tempAddr.upper().startswith(data['Assignment']):
            print(data['Organization Name'])
