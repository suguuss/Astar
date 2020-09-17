import random 
import matplotlib.pyplot as plt
import math


WALLPERCENTAGE = 20
WIDTH  = 50
HEIGHT = 50
DIAGONALS = False

wallChance = [False] * (100-WALLPERCENTAGE) + [True] * WALLPERCENTAGE 

class node:
	def __init__(self, i, j):
		#	i : w index on the grid
		#	j : h index on the grid
		#	f : cost from begining to end
		# 	g : cost from begining to current
		#	h : cost from current to end
		self.i = i
		self.j = j

		self.f = 0
		self.g = 0
		self.h = 0

		self.isWall = random.choice(wallChance)
		self.parent = None
		self.neighbours = []

		if self.isWall:
			self.color = 2
		else:
			self.color = 0

	def getNeighbours(self, grid):
		gridH = len(grid)
		gridW = len(grid[0])

		# Check all 8 neighbours N 
		#	NNN
		#	NXN
		#	NNN
		i = self.i 
		j = self.j 

		if j < gridH - 1:
			self.neighbours.append(grid[j + 1][i])
		if j > 0:
			self.neighbours.append(grid[j - 1][i])
		if i < gridW - 1:
			self.neighbours.append(grid[j][i + 1])
		if i > 0:
			self.neighbours.append(grid[j][i - 1])
		if DIAGONALS:
			if j < gridH - 1 and i < gridW - 1:
				self.neighbours.append(grid[j + 1][i + 1])
			if j < gridH - 1 and i > 0:
				self.neighbours.append(grid[j + 1][i - 1])
			if j > 0 and i < gridW - 1:
				self.neighbours.append(grid[j - 1][i + 1])
			if j > 0 and i > 0:
				self.neighbours.append(grid[j - 1][i - 1])
		return self.neighbours

def heuristic(a, b):
	dist = math.dist([a.i, a.j], [b.i, b.j])
	return dist

openSet = []
closeSet = []
w = WIDTH
h = HEIGHT
# Initialize the grid of nodes
grid = [[node(i, j) for i in range(w)] for j in range(h)]

# Create the start node
start = grid[0][0]
start.isWall = False
start.color = 10

# Create the end node
end = grid[h - 1][w - 1]
end.isWall = False
end.color = 10

foundPath = False

# Grid without path to be displayed
displayGrid = [[grid[y][x].color for x in range(w)] for y in range(h)]


openSet.append(start)
while openSet != []:
	# Selecting the next node
	winner = 0
	for x in range(len(openSet)):
		if openSet[x].f < openSet[winner].f:
			winner = x
	current = openSet[winner]

	# Check if we're at the end
	if current.j == end.j and current.i == end.i:
		print("done")
		foundPath = True
		current = current.parent
		while current.parent:
			current.color = 5
			current = current.parent
		break
	
	# Remove the dot we're testing from the openset
	openSet.remove(current)
	closeSet.append(current)

	neighbours = current.getNeighbours(grid)

	for neighbour in neighbours:
		# If the neighbour is not and wall and hasn't been tested yet
		if neighbour not in closeSet and not neighbour.isWall:
			tempG = current.g + 1
			newPath = False
			if neighbour in openSet:
				if tempG < neighbour.g:
					neighbour.g = tempG
					newPath = True
			else:
				neighbour.g = tempG
				openSet.append(neighbour)
				newPath = True
			
			if newPath:
				neighbour.h = heuristic(neighbour, end)
				neighbour.f = neighbour.g + neighbour.f
				neighbour.parent = current

if not foundPath:
	print("no Path")
	current = current.parent
	while current.parent:
		current.color = 5
		current = current.parent


# Display the path
# Grid with the path to be displayed
displayGrid2 = [[grid[y][x].color for x in range(w)] for y in range(h)]

fig = plt.figure()

fig.add_subplot(1,2,1)
plt.imshow(displayGrid)
fig.add_subplot(1,2,2)
plt.imshow(displayGrid2)
plt.show()