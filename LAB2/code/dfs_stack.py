import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    """
    Read the csv file and Iterate each
    row and create the graph
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
    """
    Initialize some datastructure to implement the dfs 
    """
    stack = [(start, 0)]
    visit = {start: None}
    dist = {start: 0}
    num_visited = 0
    """
    Implement the DFS using a stack. Each element in the stack is a tuple containing
    the current node and the total distance traveled to reach that node.
    `visit` tracks the parent node of each visited node, enabling path reconstruction.
    `dist` keeps track of the shortest distance from the start node to each visited node.
    """
    while stack:
        cur_node, cur_dis = stack.pop()  
        if cur_node == end:
            break
        num_visited += 1
        for neighbor, dis in graph.get(cur_node, []):
            if neighbor not in visit:
                visit[neighbor] = cur_node
                dist[neighbor] = dis + cur_dis
                stack.append((neighbor, dis + cur_dis))  
    """
    Start with end node usr visit to construct the path
    and reverse it and return path,total_dist,num_visited
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = visit[current]
    path.reverse() 
    total_dist = dist[end]
    return path, total_dist, num_visited
    # End your code (Part 2)


if __name__ == '__main__':
    #path, dist, num_visited = dfs(2270143902, 1079387396)
    path, dist, num_visited = dfs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
