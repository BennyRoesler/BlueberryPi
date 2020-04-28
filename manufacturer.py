import pandas as pd

def getMan(macAddr):
    tempAddr = macAddr.replace(':', '')
    file = pd.read_csv("manufacturerOUI.csv")
    df = file[['Assignment', 'Organization Name']]

    for index, data in df.iterrows():
        if tempAddr.upper().startswith(data['Assignment']):
            print(data['Organization Name'])

