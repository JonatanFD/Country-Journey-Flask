from data.constantes import *
import heapq
import json

def getHeuristics():
    graph_dict = {}
    cities = json.load(open(CITIES_JSON_NO_MERCATOR, 'r'))

    for city in cities:
        name = f"{city['city']},{city['country']}"
        graph_dict[name] = city["altitude"]
        pass

    return graph_dict

def heuristic(node, graph_dict):
    altitude = graph_dict[node]
    return altitude

def readGraph():
    with open(GRAPH_JSON_FILE, 'r') as file:
        return json.load(file)
    
def astar(graph, start, goal):
    visited = set()
    queue = [(0, start, [])]

    heuristics = getHeuristics()
    
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        
        if node in visited:
            continue
        
        path = path + [node]
        visited.add(node)
        
        if node == goal:
            return (cost, path)
        
        for neighbor in graph[node]:
            weight = graph[node][neighbor]

            if neighbor not in visited:
                total_cost = cost + weight + heuristic(neighbor, heuristics)
                heapq.heappush(queue, (total_cost, neighbor, path))
    
    return float("inf"), []


def filterGraphByCountries(countries):
    graph = readGraph()
    if len(countries) == 0:
        return graph

    countries = set(countries)
    filtered_graph = {}

    for origin in graph:
        origin_country = origin.split(",")[1].strip()
        
        if origin_country not in countries:
            continue

        filtered_graph[origin] = {}

        for destination, distance in graph[origin].items():
            destination_country = destination.split(",")[1].strip()
            
            if destination_country in countries:
                filtered_graph[origin][destination] = distance

        if not filtered_graph[origin]:
            del filtered_graph[origin]

    return filtered_graph

def createJourney(contrains):
    graph = filterGraphByCountries(contrains["countries"])
    start = contrains["from"]
    end = contrains["to"]

    cost, path = astar(graph, start, end)
    print(f"Costo: {cost}")
    print(f"Ruta: {path}")
    return {"cost": cost, "path": path}
