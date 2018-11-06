from functools import partial

graph = {
    'A' :'B C', 
    'B' : 'A C', 
    'C' : 'A B D E',
    'D' : 'C',
    'E' : 'C F',
    'F' : 'E'
}

graph_long = {
    '1': '2 7',
    '2': '3', 
    '3': '4', 
    '4': '5', 
    '5': '6 10', 
    '7': '8',
    '6': '5',
    '8': '9',
    '9': '10', 
    '10': '5 11', 
    '11': '12',
    '12': '11',
}

for node in graph:
    graph[node] = list(graph[node].split())

for n in graph_long:
    graph_long[n] = graph_long[n].split()

def search(graph, concat_func, first):
    seen = set()
    need_visit = [first]
    while need_visit:
        node = need_visit.pop(0)
        if node in seen: 
            continue
        print('I am looking at : {}'.format(node))
        seen.add(node)
        new_nodes = graph[node]
        need_visit = concat_func(new_nodes, need_visit)
    print()

def treat_new_nodes_more_important(new_nodes, old_nodes):
    return new_nodes + old_nodes

def treat_old_nodes_more_important(new_nodes, old_nodes):
    return old_nodes + new_nodes

bfs = partial(search, concat_func=treat_new_nodes_more_important)
dfs = partial(search, concat_func=treat_old_nodes_more_important)

bfs(graph, first='A')
dfs(graph, first='A')

bfs(graph_long, first='1')
dfs(graph_long, first='1')