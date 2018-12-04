import csv

def process():
    circles = ['北京地铁2号线', '北京地铁10号线']
    stations = {}
    lines = {}
    graph = {}
    with open('stations.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name, *pos = row
            stations[name] = pos


    with open('lines_clean.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name, *pos = row
            lines[name] = pos

    for station in stations:
        neighbors = []
        for line_name in lines:
            line = lines[line_name]
            if station in line:
                idx = list(line).index(station)
                if line_name in circles:
                    neighbors.append(line[(idx + len(line) - 1) % len(line)])
                    neighbors.append(line[(idx +  1) % len(line)])
                else:
                    if idx > 0:
                        neighbors.append(line[idx - 1])
                    if idx < len(line) - 1:
                        neighbors.append(line[idx + 1])
        graph[station] = neighbors

    with open('graph.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for station in graph:
            writer.writerow([station] + graph[station])

if __name__ == '__main__':
    process()