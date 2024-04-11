import pygame
pygame.font.init()

WIDTH = 900
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Nqueen visualization")
FONT = pygame.font.Font(None, 40)

RED = (255,0,0)
BLACK = (0,0,0)

class Cell:
    def __init__(self, row, col, cell_width):
        self.row = row 
        self.col = col 
        self.x = row * cell_width
        self.y = col * cell_width
        self.width = cell_width 
        self.color = (255,0,0)
        self.queen = False
    
    def has_queen(self):
        return self.queen
    
class Nqueen:
    def __init__(self, n, grid,queen_image):
        self.N = n 
        self.grid = grid 
        self.cell_width = WIDTH // n 
        self.queen_image_scaled = pygame.transform.scale(queen_image, (self.cell_width, self.cell_width))
        self.safe_states = []
        self.safe_states = []
             
    def put_queen_on(self, cell):
        cell.queen = True 
        
    def remove_queen_from(self, cell):
        cell.queen = False
        
    def is_safe(self, cell):
        row = cell.row 
        col = cell.col 
        
        for c in range(col):
            if grid[row][c].has_queen():
                return False
        
        for r in range(row):
            if grid[r][col].has_queen():
                return False
            
        for c,r in zip(range(col - 1, -1, -1), range(row-1, -1, -1)):
            if grid[r][c].has_queen():
                return False
        
        for c,r in zip(range(col-1, -1, -1), range(row+1, self.N)):
            if grid[r][c].has_queen():
                return False
        
        return True
     
    def draw_grid_with_queen(self):
  
        for row in self.grid:
            for cell in row:
                if(cell.has_queen()):
                    WIN.blit(self.queen_image_scaled, [cell.x, cell.y, cell.width, cell.width])
                    
                else:
                    rect = [cell.x, cell.y, cell.width, cell.width]
                    pygame.draw.rect(WIN,(255,255,255), rect, width=0)
            draw_grid(self.N)
            
        pygame.display.update()
        pygame.time.delay(500)
                
    def found_solution(self):
        self.safe_states.append(grid)
        stop = True
        message = "SOLUTION FOUND, PRESS [SPACE BAR] TO CONTINUE."
        text_surface = FONT.render(message, True, (0, 0,0,0))  
        text_rect = text_surface.get_rect()
        # Put the message at the center.
        text_rect[1] += WIDTH//2
        WIN.blit(text_surface, text_rect)
        pygame.display.update()
        while(stop):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        stop = False
        
    def solve_n_queen(self):
        self.solve(grid, 0)
        return self.safe_states
        
    def solve(self, grid, col):
        if col >= self.N:
            self.found_solution();        
            return 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        for row in range(self.N):
            cell = grid[row][col]
            if(self.is_safe(cell)):
                self.put_queen_on(cell)
                
                self.draw_grid_with_queen()
                
                self.solve(grid, col+1)
                self.remove_queen_from(cell)
                 
def make_grid(n):
    cell_width = WIDTH // n 
    grid = []
    for row in range(n) :
        grid.append([])
        for col in range(n):
            cell = Cell(row, col, cell_width)
            grid[row].append(cell)
    return grid

def draw_grid(rows):
    cols = rows 
    gap = WIDTH // rows 
    for row in range(rows):
        pygame.draw.line(WIN, RED, (0,row * gap), (WIDTH, row * gap), width=1)
    for col in range(cols):
        pygame.draw.line(WIN, RED, (col * gap, 0), (col * gap, WIDTH), width=1)

if __name__ == "__main__":
    
    n=5
    grid_width = 2
    grid = make_grid(n)
    queen_image = pygame.image.load('queen_image2.jpeg')
    nqueen = Nqueen(n, grid, queen_image)
    
    runing = True
    while(runing):
        draw_grid(n)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
        
        safe_states = nqueen.solve_n_queen()
        pygame.display.update()
        pygame.time.delay(1000)
    
        runing = False
    print(len(safe_states))
        
        
    
    
    