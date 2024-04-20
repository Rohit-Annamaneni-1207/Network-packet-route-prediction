# DN_project_route_trace

Data pre-processing and training as well as exporting models for Advanced Packet Route Visualizer

# Data generation

Wrote a python script that logs tracert commands and writes to a csv file to generate the dataset. The script additionally uses API requests to log the city and location associated with the source and destination ip addresses of a ping.

# Dataset feature sample

![image](https://github.com/Rohit-Annamaneni-1207/Network-packet-route-prediction/assets/82631318/9c29d9cb-1427-4d44-887f-0ff08d3d7f6f)

# Classification task

Label encoder is used to form classes from city names

#Models used and results

## Naive Bayes

![image](https://github.com/Rohit-Annamaneni-1207/Network-packet-route-prediction/assets/82631318/99ae7ff6-09d7-4c4b-b7c3-ccf06217feb6)

The accuracy on test set was 50%

## Decision Tree

![image](https://github.com/Rohit-Annamaneni-1207/Network-packet-route-prediction/assets/82631318/2bf9c069-dfbf-4753-950e-0ffbc4dd1369)

The accuracy on test set was 90.06%

## Random forest

![image](https://github.com/Rohit-Annamaneni-1207/Network-packet-route-prediction/assets/82631318/7c0e5938-dcda-4e56-becb-0314a713a3c8)

The accuracy on test set was 90.06%

## Neural networks

![image](https://github.com/Rohit-Annamaneni-1207/Network-packet-route-prediction/assets/82631318/8cd746e3-94f9-46d9-bb95-4284807edd46)

The accuracy on test set was 87.34%



Front-end visualizer: https://github.com/prateekin/Geotraceroute
