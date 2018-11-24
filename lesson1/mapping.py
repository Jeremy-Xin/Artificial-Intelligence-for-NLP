import networkx
import matplotlib.pyplot as plt

BJ = 'Beijing'
SZ = 'Shenzhen'
GZ = 'Guangzhou'
WH = 'Wuhan'
HLG = 'Heilongjiang'
NY = 'New York City'
CM = 'Chiangmai'
SG = 'Singapore'

air_route = {
    BJ : {SZ, GZ, WH, HLG, NY}, 
    GZ : {WH, BJ, CM, SG},
    SZ : {BJ, SG},
    WH : {BJ, GZ},
    HLG : {BJ},
    CM : {GZ},
    NY : {BJ}
}
air_route = networkx.Graph(air_route)
networkx.draw(air_route, with_labels=True)
plt.show()

def search_desitination(graph, start, destination):
    pathes = [[start]]
    choosen_pathes = []
    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]
        
        # get new lines
        for city in graph[froniter]:
            if city in path:
                continue
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination:
                choosen_pathes.append(new_path)
        
    return choosen_pathes

def draw_route(cities): 
    print(' ✈️ -> '.join(cities))

result = search_desitination(air_route, SZ, CM)
for cities in result:
    draw_route(cities)