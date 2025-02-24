import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
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
    Initialize some datastructure to implement the bfs 
    """
    queue=[(start,0)]
    visit={start:None}
    dist={start:0}
    num_visited=0
    """
    iterate queue and find update the information of node
    use visit to record the parents 
    usr dist to caculate the distance to the neighbor
    add the neighbor to the queue and updata the distance
    """
    while queue:
        cur_node,cur_dis=queue.pop(0)
        if cur_node==end:
            break
        num_visited += 1
        for neighbor,dis in graph.get(cur_node,[]):
            if neighbor not in visit:
                visit[neighbor]=cur_node
                dist[neighbor]=dis+cur_dis
                queue.append((neighbor,dis+cur_dis))
    """
    Start with end node usr visit to construct the path
    and reverse it and return path,total_dist,num_visited
    """
    path=[]
    current=end
    while current is not None:
        path.append(current)
        current=visit[current]
    path.reverse() 
    total_dist=dist[end]
    num_visited=num_visited
    return path,total_dist,num_visited
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
