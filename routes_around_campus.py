"""
Ethan Richards
CSCI 101 - Create Project: Routes Around Campus
Reference: Sumner Evans (Mines Alum + Adjunct Professor)
Reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
Reference: https://towardsdatascience.com/introduction-to-priority-queues-in-python-83664d3178c3
Reference: https://www.w3schools.com/python/python_dictionaries.asp
"""
from queue import PriorityQueue

"""
Calculate all optimal routes via Dijkstra's Algorithm
given a graph of each vertex and start location.

The graph must have all of the vertex's respective
vertices and the weight of the edge in order to get there.

Returns a tuple of a dictionary of all vertices with 
the optimal distance to get there and a dictionary with
all previous vertices visited to get there from the start_location.
"""
def calculate_routes(graph, start_location):
    # Distances, stored as distance from source to vertex
    dist = { start_location:0 }

    # All previous nodes visited
    prev = {}

    # Create priorityqueue and look through graph vertices
    pqueue = PriorityQueue()
    for vertex in graph:
        if vertex != start_location:
            # Set defaults - if vertex isn't starting location, it's infinity distance away
            dist.update({ vertex:1000000000 })
            prev.update({ vertex:None })

        pqueue.put((vertex, dist[vertex]))

    # While priorityqueue isn't empty
    while not pqueue.empty():
        # Get the current best vertex
        current = pqueue.get()
        current_node, current_weight = current

        # For each adjacent vertex
        for node, weight in graph[current_node]:
            path = dist[current_node] + weight

            # If new optimal path is less than the previous distance stored, replace it!
            if path < dist[node]:
                dist[node] = path
                prev[node] = current_node
                pqueue.put((node, path))

    return (dist, prev)

# Get the inputted data!
map_file = str(input("MAP FILE> "))
walking_speed = float(input("WALKING SPEED> "))
start_location = input("START LOCATION> ") 
end_location = input("END LOCATION> ")

# Unpack file and assemble graph
graph = {}
file = open(map_file, 'r')

for line in file:
    vertices = line.split()

    # If vertex has no adjacent vertices, still add it
    if vertices[1] == '0':
        graph.update({vertices[0]:{}})
    else:
        adjacent_array = []
        for i in range(1, len(line.split())):
            adjacent = line.split()[i].split(",")

            vertex = adjacent[0]
            weight = adjacent[1]

            # Build array of adjacent vertices and their weights
            if graph.get(vertices[0]) != None:
                for element in graph.get(vertices[0]):
                    if element not in adjacent_array:
                        adjacent_array.append(element)

            adjacent_array.append((vertex, int(weight)))

            # Update graph!
            graph.update({vertices[0]:adjacent_array})

file.close()

distances, previous_nodes = calculate_routes(graph, start_location)

for vertex in distances:
    if end_location not in distances:
        print("Can't find the specified end location! Make sure your capitalization and spelling is correct.")
        break
    
    if vertex == end_location:
        best_length_ft = float(distances[vertex])

        # Divide by 5280 to get miles!
        best_length = float(best_length_ft / 5280)

        # Minutes it takes to get there = (best length / walking_speed) * 60
        minutes = float(best_length / walking_speed) * 60

        # Store nodes in path array to later display
        path = []
        current_node = end_location

        while current_node != start_location:
            current_node = previous_nodes.get(current_node)
            path.append(current_node)

        path.reverse()
        path.append(end_location)

        # Make display string
        path_string = ""
        for i in range(len(path)):
            if i + 1 >= len(path):
                path_string += str(path[i])
            else:
                path_string += str(path[i]) + " -> "

        print(f"The most efficient distance to {end_location} is {round(best_length, 3)}mi ({best_length_ft}ft)!")
        print(f"It would take you approximately {round(minutes, 3)} minutes to walk there.")
        print(f"You should take the following path: {path_string}")
