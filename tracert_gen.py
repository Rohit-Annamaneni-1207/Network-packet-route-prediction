# from IPython.display import display
from subprocess import Popen, PIPE
import pandas as pd
import requests
import socket
import os
import json



target = "amazon"
token = "761eab6307df4b" #Rohit
token = "0b64f7f2163fa5" #Prateek

json_file = open("sessions_run.json", "r")
data = json.load(json_file)

session = data[target]["sessions_run"]
expected_sessions = data[target]["expected_sessions"]
hostname = socket.gethostname()
src = socket.gethostbyname(hostname)
output_path = "route_data.csv"
host = data[target]["url"]

defaultRTT = 25

src_location = []

# atexit.register(exit_handler, target, data, session)

json_file.close()

while (session < expected_sessions):

    def remove_items(test_list, item):
        res = [i for i in test_list if i != item]
        return res

    # dest = socket.gethostbyname(host)
    dest = target
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

        ip = output_lines[1][4]
        r_url = f"https://ipinfo.io/{ip}?token={token}"
        r = requests.get(r_url)
        json_obj = r.json()
        src_location.append(json_obj['region'])
        src_location.append(json_obj['region'])
        src_location.append(json_obj['country'])

        print(src_location)


    # for i in range(len(output_lines)):
    i = 0
    while True:

        if i == len(output_lines):
            break

        if 'timed' in output_lines[i]:
            output_lines.pop(i)
            # i += 1
            continue
            # output_lines[i] = [output_lines[i][0]] + ['*', '*', '*'] + ['Request_timed_out']
            # abort = True
        ip = output_lines[i][4]
        r_url = f"https://ipinfo.io/{ip}?token={token}"
        r = requests.get(r_url)
        json_obj = r.json()
        print("=====================================================================")
        print(json_obj)
        print(ip)
        
        if 'Request_timed_out' in output_lines[i]:
            output_lines[i].append("-")
            output_lines[i].append("-")
            output_lines[i].append("-")

        elif "bogon" not in json_obj:
            # if json_obj['city'] == "Deoli":
            #     output_lines[i].append(json_obj['region'])
            #     output_lines[i].append(json_obj['region'])
            #     output_lines[i].append(json_obj['country'])
            # else:
                output_lines[i].append(json_obj['city'])
                output_lines[i].append(json_obj['region'])
                output_lines[i].append(json_obj['country'])

        else:
            output_lines.pop(i)
            # i += 1
            continue

        output_lines[i] = [session]+[src]+ src_location +[dest]+output_lines[i]  
        print(output_lines[i])
        i += 1

        print("=====================================================================")

    for i in range(len(output_lines)):

        output_lines[i][6] = i+1
        output_lines[i][0] = int(output_lines[i][0])
        rtt_set = {output_lines[i][7], output_lines[i][8], output_lines[i][9]}
        rtt_set.discard("*")

        if len(rtt_set) > 0:
            rtt = int(list(rtt_set)[0])
        else:
            rtt = defaultRTT

        if output_lines[i][7] == "*":
            output_lines[i][7] = rtt

        if output_lines[i][8] == "*":
            output_lines[i][8] = rtt

        if output_lines[i][9] == "*":
            output_lines[i][9] = rtt

        # output_lines[i][7], output_lines[i][8], output_lines[i][9] = int(output_lines[i][7]), int(output_lines[i][8]), int(output_lines[i][9])

        avg_rtt = (int(output_lines[i][7]) + int(output_lines[i][8]) + int(output_lines[i][9]))//3
        output_lines[i] = output_lines[i][:7] + [avg_rtt] + output_lines[i][10:]

    df = pd.DataFrame(output_lines, columns=["session_no","src","src_city","src_region","src_country","dest","Hop_No", "avg_rtt", "IP_Address", "City", "Region_Name", "Country"])
    # display(df)
    # df.style
    print("============================================")
    print(df.head(20))

    
    session += 1
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
    
