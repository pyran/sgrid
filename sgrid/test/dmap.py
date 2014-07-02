# /usr/bin/env python3

class DungeonMap:
	def __init__(self):
		self.map = {}
	# https://www.python.org/doc/essays/graphs/

    def addAdjLocs(self, direction, adjacent_location_object):

        self.adjLocs[str(direction)] = adjacent_location_object
	# A recursive function used to find a path from start to end node specified.

	# Note that while the user calls find_graph() with three arguments, it calls 
	# itself with a fourth argument: the path that has already been traversed. The 
	# default value for this argument is the empty list, '[]', meaning no nodes have
	# been traversed yet. This argument is used to avoid cycles (the first 'if' 
	# inside the 'for' loop). The 'path' argument is not modified: the assignment 
	# "path = path + [start]" creates a new list. If we had written 
	# "path.append(start)" instead, we would have modified the variable 'path' in 
	# the caller, with disastrous results. (Using tuples, we could have been sure 
	# this would not happen, at the cost of having to write "path = path + (start,)"
	# since "(start)" isn't a singleton tuple -- it is just a parenthesized 
	# expression.)
	def find_path(graph, start, end, path=[]):
		path = path + [start]
		if start == end:
			return path
		# The second 'if' statement is necessary only in case there are nodes that 
		# are listed as end points for arcs but that don't have outgoing arcs 
		# themselves, and aren't listed in the graph at all. Such nodes could also 
		# be contained in the graph, with an empty list of outgoing arcs, but 
		# sometimes it is more convenient not to require this.
		if not graph.has_key(start):
			return None
		for node in graph[start]:
			if node not in path:
				newpath = find_path(graph, node, end, path)
				if newpath: return newpath
		return None

	# function to return a list of all paths (without cycles) instead of the first
	# path it finds
	def find_all_paths(graph, start, end, path=[]):
		path = path + [start]
		if start == end:
			return [path]
		if not graph.has_key(start):
			return []
		paths = []
		for node in graph[start]:
			if node not in path:
				newpaths = find_all_paths(graph, node, end, path)
				for newpath in newpaths:
					paths.append(newpath)
		return paths

	# Find the shortest path
	def find_shortest_path(graph, start, end, path=[]):
		path = path + [start]
		if start == end:
			return path
		if not graph.has_key(start):
			return None
		shortest = None
		for node in graph[start]:
			if node not in path:
				newpath = find_shortest_path(graph, node, end, path)
				if newpath:
					if not shortest or len(newpath) < len(shortest):
						shortest = newpath
		return shortest

	# Check if node to travel to is adjacent
	def check_adj(graph, start, end):
		if end in graph[start]:
			return True
		else:
			return False

	# test runs
	if __name__ == '__main__':
		graph = {
		'A': {'N':'B', 'S':'C'},
		'B': ['C','D'],
		'C': ['D'],
		'D': ['C'],
		'E': ['F'],
		'F': ['C']}

		# x = find_path(graph, 'A','D')
		# print(x)

		# y = find_all_paths(graph, 'A','D')
		# print(y)

		# z = find_shortest_path(graph, 'A', 'D')
		# print(z)

		# a = check_adj(graph, 'A', 'C')
		# print(a)
		# b = check_adj(graph, 'A', 'D')
		# print(b)
		curr = 'A'
		x = 'E'

		try:
			print(graph[curr][x])
		except KeyError:
			print("you can't go {}").format(x)

		if 'B' in graph['A']:
			print(True)