import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    """
    Read the graph and huristic value from the CSV file, converting distances 
    and speeds into time costs.Convert km/h to m/s,and the distance change into
    time_cost by time=distance/speed
    """
    graph = {}
    max_speed = 0  
    with open(edgeFile, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            num1, num2, distance, speed = int(row[0]), int(row[1]), float(row[2]), float(row[3])
            speed_m_s = speed * 1000 / 3600  
            max_speed = max(max_speed, speed_m_s)
            if num1 not in graph:
                graph[num1] = []
            graph[num1].append((num2, distance / speed_m_s))  

    heuristic = {}
    with open(heuristicFile, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            node = int(row[0])
            h_value = float(row[3]) / max_speed #CHANG THE row[?] FOR ID1/2/3
            heuristic[node] = h_value
    """
    Initialize some datastructure to implement the astar_time 
    """
    queue = [(heuristic.get(start, 0), 0, start)]
    visited = set()
    parent = {start: None}
    time_so_far = {start: 0}
    num_visited = 0
    """
    Is same as a star but the heuristic value is implement by speed and the
    distance change into time_cost
    """
    while queue:
        _, current_time, current_node = heapq.heappop(queue)
        if current_node == end:
            break

        if current_node in visited:
            continue

        visited.add(current_node)
        num_visited += 1

        for neighbor, time_cost in graph.get(current_node, []):
            if neighbor not in visited:
                new_time = current_time + time_cost
                if neighbor not in time_so_far or new_time < time_so_far[neighbor]:
                    time_so_far[neighbor] = new_time
                    parent[neighbor] = current_node
                    heapq.heappush(queue, (new_time + heuristic.get(neighbor, float('inf')), new_time, neighbor))

    """
    Start with end node usr visit to construct the path
    and reverse it and return path,total_time,num_visited
    """
    path = []
    total_time = 0
    current = end
    if current in parent:
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        total_time = time_so_far[end]
    return path, total_time, num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path,time, num_visited = astar_time(2270143902, 1079387396)
    #path,time, num_visited = astar_time(426882161, 1737223506)
    #path,time, num_visited = astar_time(1718165260,8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
