import csv
import math

stations = {}
with open('stations.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name, *pos = row
        stations[name] = pos

def get_station_distance(st1, st2):
    dx = int(stations[st1][0]) - int(stations[st2][0])
    dy = int(stations[st1][1]) - int(stations[st2][1])
    return int(math.sqrt(pow(dx, 2) + pow(dy, 2)))

dic = {}
for s1 in stations:
    for s2 in stations:
        dis = get_station_distance(s1, s2)
        dic[s1,s2] = dis

with open('distance.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for s1,s2 in dic:
        writer.writerow([s1,s2,dic[s1,s2]])