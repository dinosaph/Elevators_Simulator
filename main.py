import time, random
import numpy as np

# Setting up simulation data
OBSERVATION_COUNT = 10
BUILDING_LEVELS = 11
ROOMS_PER_LEVEL = 30
WORKER_PER_ROOM = 1
TOTAL_CAPACITY = 2
ON_PAUSE = 0
""" 
Elevators info:
	- building level
	- running or not
	- current capacity
"""
X = { "1": [0, True, 0],
        "2": [0, True, 0],
        "3": [0, True, 0]}

BUILDING_STATS = {}

# Function that initializes rooms workers count by given initial data
def setupLevels():
	global BUILDING_LEVELS, ROOMS_PER_LEVEL, WORKER_PER_ROOM
	workers = ROOMS_PER_LEVEL * WORKER_PER_ROOM
	for i in range(BUILDING_LEVELS):
		BUILDING_STATS[str(i)] = workers
	print("[INFO] Initial workers count per building level:\n", BUILDING_STATS)

# A pretty print function
def printCurrentStats():
	global X, TOTAL_CAPACITY
	stat = ""
	for x in X.keys():
		x_state = ""
		if (X[x][1]):
			x_state = "running"
		else:
			x_state = "on pause"
		stat += "[Elevator" + x + "] is " + x_state + ". Building level -> " + str(X[x][0]) + ". Capacity -> " + str(X[x][2]) + "/" + str(TOTAL_CAPACITY) + ".\n"
	print(stat)
	print("[INFO] Current workers count per building level:\n", BUILDING_STATS)

# On each observation round the states of the elevators get changed
def updateElevatorsState():
	global ON_PAUSE, BUILDING_STATS
	choices = [True, False]
	for x in X.keys():
		# Probability of running
		running = np.random.choice(choices, 1, p=[0.65, 0.35])[0]
	#	print(running)
		if (running is False):
			# A max of 2 elevators can be on maintenance
			if (ON_PAUSE < 2):
				ON_PAUSE += 1
				# When the current elevator gets on maintenance -> workers get out on the current building floor
				BUILDING_STATS[str(X[x][0])] += X[x][2]
				X[x][2] = 0
			else:
				running = True
		X[x][1] = running
	ON_PAUSE = 0

# On each round the destinations get updated 	
def updateDestinations():
	choices = ["up", "down"]
	for x in X.keys():
		# The workers usually want to go down so the probability of that choice is higher
		dest = np.random.choice(choices, 1, p=[0.34, 0.66])
		if (X[x][0] == 0):
			dest = "up"
		#print(dest)
		# Current floor index for every elevator gets changed only if it's not on maintenance
		if (X[x][1]):
			if (dest == "up"):
				X[x][0] += 1
			else:
				X[x][0] -= 1

# On each round the current capacity of every elevator gets changed by random
def updateCapacity():
	global TOTAL_CAPACITY, BUILDING_STATS
	for x in X.keys():
		getting_out = 0
		getting_in = 0
		if (X[x][1]):
			if (X[x][2] > 0):
				# [0, available_people]
				getting_out = random.randrange(0, X[x][2])
			if ((X[x][2] + getting_out) < TOTAL_CAPACITY):
				# [0, max_possible - available_people + people_got_out]
				getting_in = random.randrange(0, TOTAL_CAPACITY - X[x][2] +getting_out)
			X[x][2] += getting_in - getting_out
			# Updating building stats per level
			BUILDING_STATS[str(X[x][0])] += getting_out - getting_in

def runElevators():
	global OBSERVATION_COUNT
	while (OBSERVATION_COUNT > 0):
		updateElevatorsState()
		updateDestinations()
		updateCapacity()
		printCurrentStats()
		time.sleep(1)
		OBSERVATION_COUNT -= 1

# Main running section
if (__name__ == "__main__"):
	print("[START] Welcome to the elevator simulator.")
	setupLevels()
	runElevators()
