import pygame
import math
from queue import PriorityQueue 

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,128)
TURQUOISE = (64,244,208)
GREY = (128, 128,128)

class Spot:
    def __init__(self, row, col, width, total_rows) :
        # Which row the spot is present at
        self.row = row 
        # Which colomn the spot is present at
        self.col = col
        # Calculation of cordinate of the spot 
        self.x = row * width
        self.y = col * width 
        # Color of the spot to ditinguish between the different type of spot
        # Whether it is source, destination, wall, vistisited etc.
        self.color = WHITE
        # Set of neighbors
        self.neighbors = []
        # Width use to draw the cube in the grid
        self.width = width
        #
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col 

    # Have we already looked at you or cosider you? -> red cube. 
    def is_closed(self):
        return self.color == RED 
    
    # Are you in the open set i.e; spot is going to be looked at in 
    # upcoming itteration. -> GREEN cube
    def is_open(self):
        return self.color == GREEN 
    
    # Are you an obstacle i.e; a wall or blocked spot -> BLACK cube
    def is_barrier(self):
        return self.color == BLACK
    
    # Are you the starting node? -> ORANGE cube
    def is_start(self):
        return self.color == ORANGE
    
    # Are you the end node? -> TURQUOISE cube
    def is_end(self):
        return self.color == TURQUOISE

    # Reset the color of spot
    def reset(self):
        self.color = WHITE 

    # We have considered this cube make it red.
    def make_closed(self):
        self.color = RED 
  
    # We have to consider it in the next itteraton make it GREEN cube
    def make_open(self):
        self.color = GREEN 
    
    # We have to treat it as wall or barrier make it BLACK cube
    def make_barrier(self):
        self.color = BLACK
    
    # Are you the starting node make ORANGE cube
    def make_start(self):
        self.color = ORANGE
    
    # Are you the end make TURQUOISE cube
    def make_end(self):
        self.color = TURQUOISE

    # After getting the shortest path we have to make a path.
    # We make it a path with color PURPLE.
    def make_path(self):
        self.color = PURPLE
    
    # Draw the cube on the screen which is given by win parameter
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    # Update the neighbor of the current node.
    def update_neighbors(self, grid):
        self.neighbors = []
        
        if self.row < self.total_rows - 1:
            # DOWN neighbor
            down_neighbor = grid[self.row + 1][self.col]
            if(not down_neighbor.is_barrier()):
                self.neighbors.append(down_neighbor)
                
        if self.row > 0:
            # UP neighbor
            up_neighbor = grid[self.row - 1][self.col]
            if(not up_neighbor.is_barrier()):
                self.neighbors.append(up_neighbor)
                
        if self.col > 0:
            # LEFT neighbor
            left_neighbor = grid[self.row][self.col - 1]
            if(not left_neighbor.is_barrier()):
                self.neighbors.append(left_neighbor)
                
        if self.col < self.total_rows -1:  # total rows and columns are equal
            # RIGHT neighbor
            right_neighbor = grid[self.row][self.col + 1]
            if(not right_neighbor.is_barrier()):
                self.neighbors.append(right_neighbor)
            
        

    # Compare two spot 
    # __lt__ stands for less than
    def __lt__(self, other):
        return False
    
# Heuristic functoin
# We gonna use manhattan distance
# d = |x2-x1| + |y2-y1|
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2-x1) + abs(y2-y2)

# We have to use a data structure which store all the spot which will be displayed on the screen.
# It will be a list of list : [ [S11,S12,...,S1n], [S21,S22,...,S2n], ..., [Sn1,Sn2,...,Snn]]
# Here row == col since we are working with cube
def make_grid(rows,width):
    cols = rows
    grid = []
    gap = width // rows
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            spot = Spot(row, col, gap, rows)
            grid[row].append(spot)
    return grid 

# Draw the grid on the screen given by the win parameter 
def draw_grid(win, rows,width):
    cols = rows 
    gap = width // rows 
    for row in range(rows):
        pygame.draw.line(win, GREY, (0,row * gap), (width, row * gap), width=1)
    for col in range(cols):
        pygame.draw.line(win, GREY, (col * gap, 0), (col * gap, width), width=1)

# Main draw function to draw everything
def draw(win, grid, rows, width):
    cols = rows 

    # We clear the screen at the beginning of every frame with one color
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    # Draw the grid line on the top of the spot drawn before
    draw_grid(win, rows, width)

    # Flip the frame that is put the frame on which spot and grid have been drawn
    pygame.display.update()
    
# Get the mouse position on the click
# Here p is mouse position
# row_number = p.x // gap, where gap is the spot width
# col_number = p.y // gap
def get_mouse_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos 
    row_number = x //gap 
    col_number = y // gap 
    return row_number, col_number



def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        
""" 
A Star Algorithm is defined here:
f(node) = h(node) + g(node)
"""

def a_star_algorithm(draw, grid, start, end):
    # Count varable to deal with tie i.e; if two nodes have same f(node) than the one which was inserted should have priority.
    count = 0
    
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    
    # Current node came from
    came_from = {}
    
    # Keep track of current shortest distance from start node to current node
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    # Keep track of predicted shortest distance from  current node to end node
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    # To keep record which nodes are in PriorityQueue
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = open_set.get()[2] 
        # For sychronization
        open_set_hash.remove(current)
        
        if current == end:
            # Draw the path 
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            # Next neighbor is one spot away
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] =  temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count  += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
      
        if current != start:
            current.make_closed()
        
    return False
        

# Main  function 
# All events, main loop  and other actions are defined here
def main(win, width):
    ROWS = 100
    grid = make_grid(ROWS, width)

    # Starting node or position is defined or not
    start = None 
    # Endgin node or positon is defined or not
    end = None 
    # Running main loop or not
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            LEFT = 0 
            CENTER = 1
            RIGHT = 2
            if pygame.mouse.get_pressed()[LEFT]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                # First define the start position
                if not start and spot != end:
                    start = spot 
                    start.make_start()

                # Followed by end position
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    
                elif spot != start and spot != end:
                    spot.make_barrier()

            # Assuming with right click user want to reset the spot i.e; undo the changes.
            elif pygame.mouse.get_pressed()[RIGHT]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None 
                elif spot == end:
                    end = None 
            
            # Press [SPACE BAR] to set the neighbor and start the algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                  
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                            
                    # Here we have to pass the draw function to A* algorithm as parameter (lamda expression)
                    # x = Lamda: print() mean ->
                    # def x():
                    #    print()
                    a_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end )
                    
                if event.key == pygame.K_c:
                    start = None 
                    end = None 
                    grid = make_grid(ROWS, width)
            
    pygame.quit()

main(WIN, WIDTH)

    

    
    
    
