def readFile():

	# Function asks the user for the name of the textfile.
	# If file can be opened, inputs all information from file into a list.
	# Returns list with all cities, routes and altitudes.

	listOfCities = []
	
	while True:
		txtfile = input("Input filename: ")
		try:
			with open(txtfile, "r") as text:
				for row in text:
					listOfCities.append((row.rstrip()).split())
				
				return listOfCities
		except IOError:
			print("The file could not be opened. Please try again")
			
def algorithm(graph, begin, end, handled=[], peaks={}, past={}):

	# Recursive algorithm which utilizes Djikstra's algorithm to find the optimal route from graph.
	# Parameter graph = dictionary with all cities, routes and altitudes
	# Parameter begin = point at which function investigates neighbouring cities, starts at 1, later the city being handled.
	# Parameter end = destination city
	# Parameter handled = list of cities that have been previously investigated.
	# Parameter peaks = dictionary with lowest altitudes found for each city.
	# Parameter past = dictionary with routes taken to each city.
	
	path = [] # list used for the final path to take
	remaining = {} # dictionary of remaining cities to investigate
	
	if begin == end: # check if in destination city
		last = end
		peak = 0

		while last != None: # start travelling the route taken backwards until arriving at the start
			path.append(last)
			if(peak < peaks[last] and peaks[last] != float('inf')): # if altitude at node is higher than the previously highest, save it
				peak = peaks[last]
			last = past.get(last, None)
		path.reverse()
		if(path[0] != '1' or path[-1] != end): # if no path is found between start and destination
			print("No path was found")
		else: # else print best path and the highest altitude of path
			print("The best path is: " + "->".join(path) + " and the highest altitude on the path is: " + str(peak))
		
	else:
		if not handled: # first iteration of function no connections between cities have been found so highest altitude can be infinite
			peaks[begin] = float('inf')
		for road in graph[begin]: # investigate all neighbouring cities
			if road not in handled: # if not handled previously
				peakOfRoad = graph[begin][road] 
				if peakOfRoad < peaks.get(road, float('inf')): # check if altitude is lower than previous peak altitude for city
					peaks[road] = peakOfRoad
					past[road] = begin
		
		handled.append(begin) # add city to list of handled cities
		for i in graph: # form remaining cities to investigate
			if i not in handled:
				remaining[i] = peaks.get(i, float('inf'))
		try:
			next = str(min(remaining, key=remaining.get))
		except ValueError:
			next = end
			
		algorithm(graph, next, end, handled, peaks, past)

def main():
	
	graph = {} # dictionary with all cities, routes and altitudes
	
	listOfCities = readFile()
	
	begin = '1' # route always begins at city 1
	end = listOfCities.pop() # get destination from last element of list
	listOfCities.pop(0)
	
	for element in listOfCities: # for-loop to add all cities and routes from list to dictionary
		if element[0] in graph:
			graph[element[0]][element[1]] = int(element[2])
			if element[1] in graph:
				graph[element[1]][element[0]] = int(element[2])
			else:
				graph[element[1]] = {element[0]: int(element[2])}
		else:
			graph[element[0]] = {element[1]: int(element[2])}
			graph[element[1]] = {element[0]: int(element[2])}
			
	algorithm(graph, begin, end[0])

	
if __name__ == "__main__":
	main()