"""Pygame coordinates and python array indices are different, 
so some coordinates / indices in this program might be confusing at first"""

import pygame
import random

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 50
ROWS, COLUMNS = int(HEIGHT / CELL_SIZE), int(WIDTH / CELL_SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator and Solver")
CLOCK = pygame.time.Clock()
FPS = 30

class Cell(object):
    def __init__(self, x, y):
        # position in matrix
        self.x = x
        self.y = y
        # keeps track of which walls are still visible
        self.walls = [True, True, True, True]
        # checks if cell has been visited during generation 
        self.generated = False
        # checks if cell is on path during solving 
        self.on_path = False
        # checks if cell has been visited during solving 
        self.visited = False

    def draw_cell(self):
        # coordinates on screen
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE
        # draws a wall if it still exists
        if self.walls[0]:
            pygame.draw.line(SCREEN, WHITE, (x, y), (x + CELL_SIZE, y), 5)
        if self.walls[1]:
            pygame.draw.line(SCREEN, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 5)
        if self.walls[2]:
            pygame.draw.line(SCREEN, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 5)
        if self.walls[3]:
            pygame.draw.line(SCREEN, WHITE, (x, y), (x, y + CELL_SIZE), 5)
        # marks blue if generated during generation
        if self.generated:
            pygame.draw.rect(SCREEN, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
        # marks green if on path during solving
        if self.on_path:
            pygame.draw.rect(SCREEN, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

    # draws a red box if this is the current cell
    def draw_current(self):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE
        pygame.draw.rect(SCREEN, RED, (x, y, CELL_SIZE, CELL_SIZE))

# maintains the current state
state = "generating"
# maze matrix of cell instances
maze = []
# stack of current cells on path
stack = []
current_x, current_y = 0, 0
# resets after the maze is solved
def reset():
    global current_x, current_y, state
    current_x = 0
    current_y = 0
    state = "generating"
    maze.clear()
    stack.clear()
    for x in range(COLUMNS):
        row = []
        for y in range(ROWS):
            cell = Cell(x, y)
            row.append(cell)
        maze.append(row)
reset()

def in_bounds(x, y):
    return 0 <= x < COLUMNS and 0 <= y < ROWS

def find_next_cell(x, y):
    # keeps track of valid neighbors
    neighbors = []
    if state == "generating":
        # loop through these two arrays to find all 4 neighbor cells
        dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
        for d in range(4):
            # add cell to neighbor list if it is in bounds and not generated
            if in_bounds(x + dx[d], y + dy[d]):
                if not maze[x + dx[d]][y + dy[d]].generated:
                    neighbors.append((x + dx[d], y + dy[d]))
        # returns a random cell in the neighbors list, or -1 -1 otherwise
        if len(neighbors) > 0:
            return neighbors[random.randint(0, len(neighbors) - 1)]
        else:
            return -1, -1
    elif state == "solving":
        # add cell to neighbor list if it is in bounds and not visited
        if in_bounds(x - 1, y):
            if not maze[x][y].walls[3] and not maze[x - 1][y].visited:
                neighbors.append((x - 1, y))
        if in_bounds(x + 1, y):
            if not maze[x][y].walls[1] and not maze[x + 1][y].visited:
                neighbors.append((x + 1, y))
        if in_bounds(x, y - 1):
            if not maze[x][y].walls[0] and not maze[x][y - 1].visited:
                neighbors.append((x, y - 1))
        if in_bounds(x, y + 1):
            if not maze[x][y].walls[2] and not maze[x][y + 1].visited:
                neighbors.append((x, y + 1))
        # returns a random cell in the neighbors list, or -1 -1 otherwise
        if len(neighbors) > 0:
            return neighbors[random.randint(0, len(neighbors) - 1)]
        else:
            return -1, -1

def remove_wall(x1, y1, x2, y2):
    # x distance between original cell and neighbor cell
    xd = maze[x1][y1].x - maze[x2][y2].x
    # to the bottom
    if xd == 1:
        maze[x1][y1].walls[3] = False
        maze[x2][y2].walls[1] = False
    # to the top
    elif xd == -1:
        maze[x1][y1].walls[1] = False
        maze[x2][y2].walls[3] = False
    # y distance between original cell and neighbor cell
    xy = maze[x1][y1].y - maze[x2][y2].y
    # to the right
    if xy == 1:
        maze[x1][y1].walls[0] = False
        maze[x2][y2].walls[2] = False
    # to the left
    elif xy == -1:
        maze[x1][y1].walls[2] = False
        maze[x2][y2].walls[0] = False

def simulate():
    global current_x, current_y, state
    if state == "generating":
        maze[current_x][current_y].generated = True
        maze[current_x][current_y].draw_current()
        next_cell = find_next_cell(current_x, current_y)
        # checks if a neighbor was returned
        if next_cell[0] >= 0 and next_cell[1] >= 0:
            stack.append((current_x, current_y))
            remove_wall(current_x, current_y, next_cell[0], next_cell[1])
            current_x = next_cell[0]
            current_y = next_cell[1]
        # no neighbor, so go to the previous cell in the stack
        elif len(stack) > 0:
            previous = stack.pop()
            current_x = previous[0]
            current_y = previous[1]
        else:
            state = "solving"
    elif state == "solving":
        maze[current_x][current_y].visited = True
        maze[current_x][current_y].on_path = True
        maze[current_x][current_y].draw_current()
        next_cell = find_next_cell(current_x, current_y)
        # checks if the maze has been solved
        if current_x == COLUMNS - 1 and current_y == ROWS - 1:
            state = "generating"
            reset()
        # checks if a neighbor was returned
        elif next_cell[0] >= 0 and next_cell[1] >= 0:
            stack.append((current_x, current_y))
            current_x = next_cell[0]
            current_y = next_cell[1]
        # no neighbor, so go to the previous cell in the stack
        elif len(stack) > 0:
            previous = stack.pop()
            maze[current_x][current_y].on_path = False
            current_x = previous[0]
            current_y = previous[1]

def draw_screen():
    SCREEN.fill(BLACK)
    for i in range(COLUMNS):
        for j in range(ROWS):
            maze[i][j].draw_cell()
    simulate()
    pygame.display.update()


def main():
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_screen()


if __name__ == "__main__":
    main()

pygame.quit()
