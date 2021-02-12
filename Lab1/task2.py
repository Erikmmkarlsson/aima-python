from search import *


farmer_problem = GraphProblem('fcgw_', '_fcgw', farmer_map)


print("Breadth first:", breadth_first_graph_search(farmer_problem).solution())

print("Depth first:",depth_first_graph_search(farmer_problem).solution())

print("Astar:",astar_search(farmer_problem).solution())
