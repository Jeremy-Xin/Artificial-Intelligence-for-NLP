import csv

def process():
    graph = {}
    with open('graph.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name, *neighbors = row
            graph[name] = neighbors

    lines = {}
    with open('lines_clean.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name, *pos = row
            lines[name] = pos

    dic = {}
    for s in graph:
        neighbors = graph[s]
        for n in neighbors:
            set1 = set()
            set2 = set()
            for line_name in lines:
                line = lines[line_name]
                if s in line:
                    set1.add(line_name)

            for line_name in lines:
                line = lines[line_name]
                if n in line:
                    set2.add(line_name)
            cross = (set1 & set2).pop()
            dic[(s, n)] = cross

    with open('intersect.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for s1,s2 in dic:
            writer.writerow([s1,s2,dic[s1,s2]])

if __name__ == '__main__':
    process()