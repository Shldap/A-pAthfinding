import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Application")

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Grid Constants
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

# Create Grid
grid = []
for row in range(GRID_SIZE):
    grid.append([0] * GRID_SIZE)


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.parent = None
        self.cost = 0
        self.heuristic = 0

    def calculate_heuristic(self, end_node):
        # Calculate the heuristic value using Euclidean distance
        self.heuristic = math.sqrt((self.row - end_node.row) ** 2 + (self.col - end_node.col) ** 2)


def find_start_node():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 1:
                return Node(row, col)


def find_end_node():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 2:
                return Node(row, col)


def generate_neighbors(node):
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for direction in directions:
        new_row = node.row + direction[0]
        new_col = node.col + direction[1]

        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
            neighbors.append(Node(new_row, new_col))

    return neighbors


def construct_path(end_node):
    path = []
    current_node = end_node

    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent

    return path[::-1]


def update_grid_with_path(path):
    for node in path:
        grid[node.row][node.col] = 4


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            cell_value = grid[row][col]

            # Left mouse button - Set start node
            if event.button == 1 and cell_value != 2:
                grid[row][col] = 1

            # Right mouse button - Set end node
            elif event.button == 3 and cell_value != 1:
                grid[row][col] = 2

            # Middle mouse button - Set/remove walls
            elif event.button == 2 and cell_value not in [1, 2]:
                grid[row][col] = 3

        # Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Trigger pathfinding algorithm
                find_path()


def draw_grid():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = grid[row][col]
            color = WHITE

            # Set colors based on cell value
            if cell_value == 1:
                color = GREEN
            elif cell_value == 2:
                color = RED
            elif cell_value == 3:
                color = BLACK
            elif cell_value == 4:
                color = YELLOW

            # Draw the cell
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.flip()


def find_path():
    # Find the start and end nodes in the grid
    start_node = find_start_node()
    end_node = find_end_node()

    # Initialize open and closed lists
    open_list = [start_node]
    closed_list = []

    while open_list:
        # Get the node with the lowest cost + heuristic value
        current_node = min(open_list, key=lambda node: node.cost + node.heuristic)

        # Move the current node from open toclosed list
        open_list.remove(current_node)
        closed_list.append(current_node)

        # Check if the current node is the end node
        if current_node == end_node:
            # Construct the path
            path = construct_path(current_node)
            update_grid_with_path(path)
            return

        # Generate neighboring nodes
        neighbors = generate_neighbors(current_node)

        for neighbor in neighbors:
            # Skip if the neighbor is a wall or already in the closed list
            if grid[neighbor.row][neighbor.col] == 3 or neighbor in closed_list:
                continue

            # Calculate the cost from the start node to the neighbor
            new_cost = current_node.cost + 1

            if neighbor not in open_list or new_cost < neighbor.cost:
                # Update the neighbor's properties
                neighbor.cost = new_cost
                neighbor.calculate_heuristic(end_node)
                neighbor.parent = current_node

                if neighbor not in open_list:
                    open_list.append(neighbor)


# Main game loop
while True:
    handle_events()
    draw_grid()
