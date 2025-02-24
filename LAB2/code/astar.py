import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    """
    Initialize the graph and heuristic dictionaries from CSV
    the heuristic need to chage when chage ID
    """
    graph = {}
    with open(edgeFile, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            source = int(row[0])
            target = int(row[1])
            distance = float(row[2])

            if source not in graph:
                graph[source] = []
            graph[source].append((target, distance))

    heuristic = {}
    with open(heuristicFile, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            node = int(row[0])
            h_value = float(row[3])#CHANG THE row[?] FOR ID1/2/3
            heuristic[node] = h_value
    """
    Initialize some datastructure to implement the astar 
    """
    queue = [(heuristic[start], 0, start)]  
    visited = set()
    parent = {start: None}
    cost = {start: 0}
    num_visited = 0
    """
    A* search implementation using a priority queue. Each queue entry is a tuple
    containing the total estimated cost (f = g + h), the current cost to reach the node (g),
    and the node itself. The heuristic value (h) is an estimate of the cost to reach the goal
    from the current node.
    """

    while queue:
        _, cur_cost, cur_node = heapq.heappop(queue)
        if cur_node == end:
            num_visited += 1
            break

        if cur_node in visited:
            continue

        visited.add(cur_node)
        num_visited += 1

        for neighbor, edge_cost in graph.get(cur_node, []):
            if neighbor not in visited:
                new_cost = cur_cost + edge_cost
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    parent[neighbor] = cur_node
                    heapq.heappush(queue, (new_cost + heuristic.get(neighbor, float('inf')), new_cost, neighbor))
    """
    Start with end node usr visit to construct the path
    and reverse it and return path,total_dist,num_visited
    """
    path = []
    current = end
    if current in parent:  
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path, cost[end], num_visited

    # End your code (Part 4)


if __name__ == '__main__':
    #path, dist, num_visited = astar(2270143902, 1079387396)
    #path, dist, num_visited = astar(426882161, 1737223506)
    path, dist, num_visited = astar(1718165260,8513026827)
    
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
