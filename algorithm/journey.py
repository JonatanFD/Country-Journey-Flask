from data.constantes import *
import heapq
import json

def get_graph_dict():
    graph_dict = {}
    cities = json.load(open(CITIES_JSON_NO_MERCATOR, 'r'))

    for city in cities:
        name = f"{city['city']},{city['country']}"
        graph_dict[name] = city
        pass

    return graph_dict

def readGraph():
    with open(GRAPH_JSON_FILE, 'r') as file:
        return json.load(file)
    
def astar(graph, start, goal):
    visited = set()
    queue = [(0, start, [])]
    graph_dict = get_graph_dict()
    
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
                total_cost = cost + weight # + heuristic(neighbor, goal, graph_dict)
                heapq.heappush(queue, (total_cost, neighbor, path))
    
    return float("inf"), []


def filterGraphByCountries(countries):
    # Lee el grafo completo desde el archivo
    graph = readGraph()
    if len(countries) == 0:
        return graph

    countries = set(countries)
    filtered_graph = {}

    for origin in graph:
        origin_country = origin.split(",")[1].strip()
        
        # Solo consideramos el origen si está en los países filtrados
        if origin_country not in countries:
            continue

        # Agregamos el nodo de origen en el grafo filtrado
        filtered_graph[origin] = {}

        for destination, distance in graph[origin].items():
            destination_country = destination.split(",")[1].strip()
            
            # Añadimos la conexión si el país del destino está en los países filtrados
            if destination_country in countries:
                filtered_graph[origin][destination] = distance

        # Si el nodo de origen no tiene conexiones en el grafo filtrado, lo eliminamos
        if not filtered_graph[origin]:
            del filtered_graph[origin]

    return filtered_graph

def createJourney(contrains):
    print(contrains)
    graph = filterGraphByCountries(contrains["countries"])
    print(graph)
    start = contrains["from"]
    end = contrains["to"]

    cost, path = astar(graph, start, end)

    return {"cost": cost, "path": path}
