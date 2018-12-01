import csv

stations = {}
lines = {}
with open('stations.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name, *pos = row
        stations[name] = pos


with open('lines_crawled.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name, *pos = row
        lines[name] = pos

cleaned_lines = {}
for line in lines:
    l = lines[line]
    cleaned_line = []
    for station in l:
        if station in stations:
            cleaned_line.append(station)

    cleaned_lines[line] = cleaned_line

with open('lines_clean.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for key in cleaned_lines:
        writer.writerow([key] + cleaned_lines[key])