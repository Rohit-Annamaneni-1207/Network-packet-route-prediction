# from IPython.display import display
from subprocess import Popen, PIPE
import pandas as pd
import requests
import socket
import os
import json

target = "google"

json_file = open("sessions_run.json", "r")
data = json.load(json_file)

session = data[target]["sessions_run"]
expected_sessions = data[target]["expected_sessions"]
hostname = socket.gethostname()
src = socket.gethostbyname(hostname)
output_path = "route_data.csv"
host = data[target]["url"]

r_url = f"http://ip-api.com/json/"

src_location = []

# atexit.register(exit_handler, target, data, session)

json_file.close()

while (session < expected_sessions):

    def remove_items(test_list, item):
        res = [i for i in test_list if i != item]
        return res

    dest = socket.gethostbyname(host)
    p = Popen(['tracert', host], stdout=PIPE)

    output_lines = []
    while True:
        line = p.stdout.readline().decode("utf-8")
        output_lines.append(line)
        print(line)

        if not line:
            break

    output_lines = output_lines[4:len(output_lines)-3]

    output_lines = [remove_items(line.split(), 'ms') for line in output_lines]

    for line in output_lines:
        if len(line) == 6:
            print(f"=====================")
            print(line.pop(4))
            print(line[4])
            print(f"=====================")
            line[4] = line[4][1:len(line[4])-1]

    # print(output_lines[1][4])

    if len(src_location) == 0:
        r = requests.get(r_url + output_lines[1][4])
        json_obj = r.json()
        src_location.append(json_obj['city'])
        src_location.append(json_obj['regionName'])
        src_location.append(json_obj['country'])

        print(src_location)


    for i in range(len(output_lines)):

        if 'timed' in output_lines[i]:
            output_lines[i] = [output_lines[i][0]] + ['*', '*', '*'] + ['Request_timed_out']
            abort = True
        r = requests.get(r_url + output_lines[i][4])
        json_obj = r.json()
        
        if 'Request_timed_out' in output_lines[i]:
            output_lines[i].append("-")
            output_lines[i].append("-")
            output_lines[i].append("-")

        elif r.json()['status'] == 'success':
            output_lines[i].append(json_obj['city'])
            output_lines[i].append(json_obj['regionName'])
            output_lines[i].append(json_obj['country'])

        else:
            output_lines[i].append('bogon')
            output_lines[i].append('bogon')
            output_lines[i].append('bogon')

        output_lines[i] = [session]+[src]+ src_location +[dest]+output_lines[i]  
        print(output_lines[i])


    df = pd.DataFrame(output_lines, columns=["session_no","src","src_city","src_region","src_country","dest","Hop_No", "RTT_1", "RTT_2", "RTT_3", "IP_Address", "City", "Region_Name", "Country"])
    # display(df)
    # df.style
    print("============================================")
    print(df.head(20))

    
    session += 1
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
    
