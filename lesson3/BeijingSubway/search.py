import csv
import networkx as nx
import math
from functools import partial

stations = {}
lines = {}
graph = {}
intersects = {}
distances = {}
with open('stations.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name, x, y = row
        stations[name] = int(x), int(y)


with open('lines_clean.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name, *pos = row
        lines[name] = pos

with open('graph.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name, *neighbors = row
        graph[name] = neighbors

with open('intersect.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        s1, s2, line = row
        intersects[s1, s2] = line

with open('distance.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        s1, s2, dis = row
        distances[s1, s2] = int(dis)

station_graph = nx.Graph(graph)

def search(graph, start, dest, strategy_func):
    pathes = [[start]]
    seen = set()
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if frontier in seen:
            continue

        for city in graph[frontier]:
            if city in path:
                continue
            new_path = path + [city]
            pathes.append(new_path)
            if is_goal(city, dest):
                return new_path, strategy_func(new_path, dest)

        pathes = sorted(pathes, key=lambda p: strategy_func(p, dest))
        seen.add(frontier)
    return [], None

def search_pruning(graph, start, dest, strategy_func):
    pathes = [[start]]
    chosen_cost = None
    chosen = []
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]

        if chosen:
            cost = strategy_func(path, dest)
            if cost >= chosen_cost:
                continue

        for city in graph[frontier]:
            if city in path:
                continue
            new_path = path + [city]
            pathes.append(new_path)
            if is_goal(city, dest):
                chosen.append(new_path)
                if chosen_cost:
                    cost = strategy_func(new_path, dest)
                    if cost < chosen_cost:
                        chosen_cost = cost
                else:
                    chosen_cost = strategy_func(new_path, dest)

        pathes = sorted(pathes, key=lambda p: strategy_func(p, dest))
    if chosen:
        return chosen[-1], strategy_func(chosen[-1], dest)
    return [], None

def is_goal(start, dest):
    return start == dest

def get_path_distance(path):
    # print('get distance', path[:5])
    distance = 0
    for i in range(len(path)):
        if i == 0:
            continue
        distance += distances[path[i - 1], path[i]]
    return distance

def min_distance_cost(pathes, dest):
    return get_path_distance(pathes) + distances[pathes[-1], dest]

def interchange_cost(pathes, dest):
    cur = None
    interchange = 0
    for i in range(len(pathes)):
        if i == 0:
            continue
        new_station = check_same_line(pathes[i], pathes[i-1])
        if cur != None and cur != new_station:
            interchange += 1
        cur = new_station
    return interchange

def time_cost(pathes, dest):
    # 假设距离50耗时一分钟 换乘时间三分钟
    return min_distance_cost(pathes, dest) / 50 + interchange_cost(pathes, dest) * 3

def min_station_cost(pathes, dest):
    # 预估站数，按照一站100距离计算
    return len(pathes) + distances[pathes[-1], dest] / 100

def check_same_line(st1, st2):
    if (st1,st2) in intersects:
        return intersects[st1, st2]
    else:
        return None

def get_path(path):
    result = []
    cur_line = None
    for i, s in enumerate(path):
        if i == len(path) - 1:
            result[-1].append(s)
            break
        line = check_same_line(path[i], path[i+1])
        if cur_line == None:
            result.append([])
            result[-1].append(line)
            result[-1].append(s)
            cur_line = line
        elif line != cur_line:
            result[-1].append(s)
            result.append([])
            result[-1].append(line)
            result[-1].append(s)
            cur_line = line
        elif line == cur_line:
            result[-1].append(s)
    return result

def print_path(path):
    if not path:
        print('没有找到路线。')
        return
    for i, line in enumerate(path):
        line_name = str(line[0])[4:]
        if i == 0:
            print('从{}-{}站出发，经过'.format(line_name, line[1]), end='')
            if len(line) >= 2:
                for station in line[2:]:
                    print('{}站，'.format(station),end='')
                print()
        elif i == len(path) - 1:
            print('换乘{}，经过'.format(line_name), end='')
            for station in line[1:-1]:
                print('{}站，'.format(station),end='')
            print()
            print('到达终点{}站。'.format(line[-1]))
        else:
            print('换乘{}，经过'.format(line_name), end='')
            for station in line[1:]:
                print('{}站，'.format(station),end='')
            print()
    print()

min_distance_search = partial(search, strategy_func=min_distance_cost)
least_interchange_search = partial(search, strategy_func=interchange_cost)
least_time_search = partial(search, strategy_func=time_cost)
min_station_search = partial(search, strategy_func=min_station_cost)

min_distance_search_pruning = partial(search_pruning, strategy_func=min_distance_cost)
least_interchange_search_pruning = partial(search_pruning, strategy_func=interchange_cost)
least_time_search_pruning = partial(search_pruning, strategy_func=time_cost)
min_station_search_pruning = partial(search_pruning, strategy_func=min_station_cost)

# path, cost = min_distance_search(graph, '西局', '望京')
# path2, cost2 = min_distance_search_pruning(graph, '西局', '望京')

# path, cost = least_interchange_search(graph, '西局', '望京')
# path2, cost2 = least_interchange_search_pruning(graph, '西局', '望京')

# path, cost = least_time_search(graph, '西局', '望京')
# path2, cost2 = least_time_search_pruning(graph, '西局', '望京')

# path, cost = min_station_search(graph, '西局', '望京')
# path2, cost2 = min_station_search_pruning(graph, '西局', '望京')

# path, cost = least_time_search(graph, '西直门', '公主坟')
# path2, cost2 = least_time_search_pruning(graph, '西直门', '公主坟')

# path, cost = least_time_search(graph, '郭公庄', '立水桥')
# path2, cost2 = least_time_search_pruning(graph, '郭公庄', '立水桥')

# path, cost = least_time_search(graph, '昌平', '十里河')
# path2, cost2 = least_time_search_pruning(graph, '昌平', '十里河')

path, cost = min_station_search(graph, '燕山', '潞城')
path2, cost2 = min_station_search_pruning(graph, '燕山', '潞城')

# path, cost = min_station_search(graph, '金安桥', '古城')
# path2, cost2 = min_station_search_pruning(graph, '金安桥', '古城')

print_path(get_path(path))
print('路径代价：', cost)
print()
print_path(get_path(path2))
print('路径代价：', cost2)
print()