from graph import Digraph,WeightedEdge,Node
# def load_map(map_filename):
#     """
#     Parses the map file and constructs a directed graph

#     Parameters:
#         map_filename : name of the map file

#     Assumes:
#         Each entry in the map file consists of the following four positive
#         integers, separated by a blank space:
#             From To TotalDistance DistanceOutdoors
#         e.g.
#             32 76 54 23
#         This entry would become an edge from 32 to 76.

#     Returns:
#         a Digraph representing the map
#     """

#     # TODO
#     print("Loading map from file...")
#     mapp = Digraph()
#     with open(map_filename) as file:
#         for line in file:
#             src,dest,Tdis,Odis= line.split(" ")
#             mapp.add_node(src)
#             # mapp.add_node(dest)
#             Magedge = WeightedEdge(src,dest,Tdis,Odis)

#     return mapp        

# print(load_map(map_filename='mit_map.txt'))

digraph = Digraph()



def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    start = Node(start)
    end = Node(end)
    if start != digraph.has_node(start) and end != digraph.has_node(end):
        raise ValueError("Nodes not available")
    curr_path,total_dis,total_outd = path
    if start == end:
        if total_dis <= best_dist:
            best_dist = total_dis
            max_dist_outdoors = total_outd
            best_path = path
            return (best_path,best_dist)
        return None
    for node in digraph.get_edges_for_node(start):
        if node not in curr_path:
            total_dis += node.get_total_distance()
            total_outd += node.get_total_distance()
            if best_dist == None or len(curr_path) <= len(best_path):
                newPath = get_best_path(digraph,node,end,path,max_dist_outdoors,best_dist,best_path)
                if newPath != None:
                    best_path = newPath
    if total_dis > best_dist:
        return None
    return (best_path,total_dis)  



print(get_best_path(digraph,str(9),str(42),15,20))
