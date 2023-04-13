import json
import numpy as np
import matplotlib.pyplot as plt

# function to convert json object to data frame 
def jsontodf(data):
    length = len(data)
    rssi = []
    snr = []
    geui = []
    for i in range(length - 1, -1, -1):
        if(data[i]['name'] == "ns.up.data.process"):
            geui.append(data[i]['data']['rx_metadata'][0]['gateway_ids']['eui'])
            rssi.append(data[i]['data']['rx_metadata'][0]['rssi'])
            if('snr' in data[i]['data']['rx_metadata'][0]):
                snr.append(data[i]['data']['rx_metadata'][0]['snr'])
            else:
                snr.append(0)
        elif(data[i]['name'] == "as.up.data.forward"):
            geui.append(data[i]['data']['uplink_message']['rx_metadata'][0]['gateway_ids']['eui'])
            rssi.append(data[i]['data']['uplink_message']['rx_metadata'][0]['rssi'])
            if('snr' in data[i]['data']['uplink_message']['rx_metadata'][0]):
                snr.append(data[i]['data']['uplink_message']['rx_metadata'][0]['snr'])
            else:
                snr.append(0)
    return rssi, snr, geui

# average every 3 fcnts
def average(lists):
    new = []
    sum = 0
    for i in range(len(lists)):
        sum = sum + lists[i]
        if((i+1)%3==0):
            new.append(sum/3)
            sum = 0
    return new


def jsontodf1(data):
    length = len(data)
    rssi = []
    snr = []
    geui = []
    for i in range(length - 1, -1, -1):
        if(data[i]['name'] == "ns.up.data.process"):
            for j in data[i]['data']['rx_metadata']:
                geui.append(j['gateway_ids']['eui'])
                rssi.append(j['rssi'])
                if('snr' in j):
                    snr.append(j['snr'])
                else:
                    snr.append(0)
        elif(data[i]['name'] == "as.up.data.forward"):
            for j in data[i]['data']['uplink_message']['rx_metadata']:
                geui.append(j['gateway_ids']['eui'])
                rssi.append(j['rssi'])
                if('snr' in j):
                    snr.append(j['snr'])
                else:
                    snr.append(0)
    return rssi, snr, geui


dragino_eui = 'A84041FFFF227F75'
sx1303_eui = '0016C001F160F149'
path_raw = 'train_data/raw'
path_processed = 'train_data/processed'

f = open(path_raw+'/t20_tx10.json')
data = json.load(f)
rssi, snr, geui = jsontodf1(data)
distance = np.arange(0, len(rssi), 3)
rssi_1 = average(rssi)
snr_1 = average(snr)
f.close()

f = open(path_raw+'/t8_tx10.json')
data = json.load(f)
length = len(data)
rssi, snr, geui = jsontodf1(data)
rssi_2, snr_2 = [[],[]], [[],[]]
for i in range(len(rssi)):
    if(geui[i] == dragino_eui):
        rssi_2[0].append(rssi[i])
        snr_2[0].append(snr[i])
    else:
        rssi_2[1].append(rssi[i])
        snr_2[1].append(snr[i]) 
rssi_2[0] = average(rssi_2[0])
snr_2[0] = average(snr_2[0])
rssi_2[1] = average(rssi_2[1])
snr_2[1] = average(snr_2[1])
del rssi_2[0][68:80]
f.close()

f = open(path_raw+'/t8_tx15.json')
data = json.load(f)
length = len(data)
rssi, snr, geui = jsontodf1(data)
rssi_3, snr_3 = [[],[]], [[],[]]
for i in range(len(rssi)):
    if(geui[i] == dragino_eui):
        rssi_3[0].append(rssi[i])
        snr_3[0].append(snr[i])
    else:
        rssi_3[1].append(rssi[i])
        snr_3[1].append(snr[i]) 
rssi_3[0] = average(rssi_3[0])
snr_3[0] = average(snr_3[0])
rssi_3[1] = average(rssi_3[1])
snr_3[1] = average(snr_3[1])
for i in range(8):
    rssi_3[0].append("Nan")
f.close()

# plot rssi-distance graph 
distance = np.arange(0, len(rssi_1)*3, 3)
fig, axs = plt.subplots(3, figsize=(15, 15))
fig.tight_layout()
axs[0].scatter(distance, rssi_1)
axs[1].scatter(distance, rssi_2[0])
axs[2].scatter(distance, rssi_3[0])
axs[0].set_title("Tx power = 10 and 20 seconds interval")
axs[1].set_title("Tx power = 10 and 8 seconds interval")
axs[2].set_title("Tx power = 15 and 8 seconds interval")

# plt.show()

# write processed to json file
rssi_1_json = json.dumps({'rssi': rssi_1, 'distance': distance.tolist()})
rssi_2_json = json.dumps({'rssi': rssi_2[0], 'distance': distance.tolist()})
rssi_3_json = json.dumps({'rssi': rssi_3[0], 'distance': distance.tolist()})
with open(path_processed+'/t20_tx10.json', 'w') as f:
    json.dump(rssi_1_json, f)
with open(path_processed+'/t8_tx10.json', 'w') as f:
    json.dump(rssi_2_json, f)
with open(path_processed+'/t8_tx15.json', 'w') as f:
    json.dump(rssi_3_json, f)