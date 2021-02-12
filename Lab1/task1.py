from search import *

romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)


print("Best first exploration:")

best_first_graph_search_print(romania_problem, lambda node: node.state)

#Performing the search algorithms
breadth_s = breadth_first_graph_search(romania_problem).solution()
breadth_c = breadth_first_graph_search(romania_problem).path_cost
print("Breadth first:" , breadth_s, breadth_c)

depth_s = depth_first_graph_search(romania_problem).solution()
depth_c = depth_first_graph_search(romania_problem).path_cost
print("Depth first:" ,depth_s, depth_c)

uniform_s = uniform_cost_search(romania_problem, True).solution()
uniform_c = uniform_cost_search(romania_problem).path_cost
print("uniform cost:" , uniform_s, uniform_c)

best_s = best_first_graph_search(romania_problem, lambda node: node.state, True ).solution()
best_c = best_first_graph_search(romania_problem, lambda node: node.state ).path_cost
print("Best first:" , best_s, best_c)

astar_s = astar_search(romania_problem, None, True).solution()
astar_c = astar_search(romania_problem).path_cost
print("A*:" , astar_s, astar_c)




