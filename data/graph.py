import json
from data.constantes import *

def getGraph():
    graph = {}

    with open(ROUTES_JSON_FILE, 'r') as file:
        data = json.load(file)

        for route in data:
            city1 = route["from"]
            city2 = route["to"]
            distance = route["distance"]

            if city1 not in graph:
                graph[city1] = {}

            if city2 not in graph:
                graph[city2] = {}

            graph[city1][city2] = distance
            graph[city2][city1] = distance
    
    with open(GRAPH_JSON_FILE, 'w') as file:
        json.dump(graph, file, indent=4)

    return graph

getGraph()