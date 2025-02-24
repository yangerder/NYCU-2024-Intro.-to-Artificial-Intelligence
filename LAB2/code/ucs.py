import csv
import heapq
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    """
    Read the csv file and Iterate each
    row and create the graph
    """
    graph={}
    with open(edgeFile,mode='r') as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            source=int(row[0])
            target=int(row[1])
            distance=float(row[2])    

            if source not in graph:
                graph[source]=[]
           
            graph[source].append((target,distance))
    """
    Initialize some datastructure to implement the ucs
    """
    queue=[(0,start)]
    visited=set()
    parent={start:None}
    cost={start:0}
    num_visited=0
    """
    Implement the UCS using a priority queue (min-heap). Each element in the queue
    is a tuple containing the total cost to reach the current node and the node itself.
    `visited` is a set that tracks which nodes have been visited to prevent revisiting.
    `parent` stores the parent of each node for path reconstruction.
    `cost` keeps track of the minimum cost to reach each node from the start node.
    """
    while queue:
        cur_cost,cur_node=heapq.heappop(queue)
        num_visited+=1
        if cur_node==end:
            break
        if cur_node in visited:
            continue
        visited.add(cur_node)
        for neighbor,edge_cost in graph.get(cur_node,[]):
            if neighbor not in visited:
                new_cost=cur_cost+edge_cost
                if neighbor not in cost or new_cost <cost[neighbor]:
                    cost[neighbor]=new_cost
                    parent[neighbor]=cur_node
                    queue.append((new_cost,neighbor))

    """
    Start with end node usr visit to construct the path
    and reverse it and return path,total_dist,num_visited
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()

    return path, cost[end], num_visited

    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    #path, dist, num_visited = ucs(426882161, 1737223506)
    #path, dist, num_visited = ucs(1718165260,8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
