"""
This script provides a simple command-line-output version of the least-cost path solution
using randomly-generated notional arrays. We implement the A* search algorithm.
"""

# Import the necessary libraries
import numpy as np
import heapq  # For priority queue in A* search

# A* search algorithm function
def astar(start, end, h, g):
    closed_set = set()  # The set of grid cells already evaluated
    open_set = [(0, start)]  # Priority queue for grid cells to be evaluated, initialized with the start cell
    came_from = {}  # Data structure to hold parent-child relationships between cells
    g_costs = {start: 0}  # Cost from start to this cell, initialized for start cell
    
    # Continue until there are no more cells to evaluate
    while open_set:
        _, current = heapq.heappop(open_set)  # Pop the cell with the lowest f score value

        # If the end cell is reached, reconstruct and return the path
        if current == end:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        # Generate neighbors of the current cell
        neighbors = []
        y, x = current
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Top, Bottom, Left, Right
            neighbor = y + dy, x + dx
            
            # Check boundary conditions
            if 0 <= neighbor[0] < h.shape[0] and 0 <= neighbor[1] < h.shape[1]:
                neighbors.append(neighbor)
        
        # Evaluate neighbors
        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            tentative_g = g_costs[current] + g[neighbor]  # Compute tentative g score for neighbor
            
            # Check if this path to neighbor is better, shorter or "equal"
            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + h[neighbor]  # f = g + h
                
                # If neighbor not in open set, add it
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score, neighbor))
       
        # Add current cell to closed set
        closed_set.add(current)

    # If there is no path to the end cell, return an empty list
    return []

# Initialize the grid dimensions
w = 5
h = 5

# Define start and end locations
start = (h-1, 0)  # Lower left corner
end = (0, w-1)  # Upper right corner

# Initialize the cost and distance grids
a = np.zeros((w, h))
dist = np.zeros(a.shape, dtype=np.int8)

# Calculate Manhattan distance for all cells from the end location
for y, x in np.ndindex(a.shape):
    dist[y][x] = abs((end[1]-x) + (end[0]-y))

# Generate a cost grid using random "terrain" values added to the distance grid
cost = np.random.randint(1, 16, (w, h)) + dist

# Output the cost grid
print("COST GRID (Value + Distance)")
print(cost)
print()

# Find the least-cost path
path = astar(start, end, cost, dist)

# Create a grid to visualize the path, populate it and print
path_grid = np.zeros(cost.shape, dtype=np.uint8)
for y, x in path:
    path_grid[y][x] = 1
path_grid[end] = 1

print()
print("PATH GRID: 1=path")
print(path_grid)
