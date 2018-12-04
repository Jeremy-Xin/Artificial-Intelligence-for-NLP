import re
import csv

dic = {}
f = open('map.html', 'r')
content = f.read()
stations = re.findall(r'<ellipse\s(.*?)></ellipse>', content)
for each in stations:
    name = re.search('name="(.*?)"', each).group(1)
    x = re.search('sx="(.*?)"', each).group(1)
    y = re.search('sy="(.*?)"', each).group(1)
    dic[name] = int(float(x)), int(float(y))

stations = re.findall(r'<image\s(.*?)></image>', content)
print(len(stations))
for each in stations:
    name = re.search('name="(.*?)"', each)
    x = re.search('sx="(.*?)"', each)
    y = re.search('sy="(.*?)"', each)
    if name and x and y:
        name = name.group(1)
        x = int(float(x.group(1)))
        y = int(float(y.group(1)))
        dic[name] = int(float(x)), int(float(y))

with open('stations.csv', 'w', newline='') as csvfile:
    fieldnames = ['station_name', 'position_x', 'position_y']
    writer = csv.writer(csvfile, delimiter=',')
    for key in dic:
        writer.writerow([key, dic[key][0], dic[key][1]])