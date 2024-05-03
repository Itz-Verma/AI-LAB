import sys

class Nqueens:
    def __init__(self,n):
        self.N = n
        self.safe_configs = []
   
   # Initialising Board which as no queen place yet
    def init_curr_board_config(self):
        return [['.' for _ in range(self.N)] for _ in range(self.N)]

    # Check the current place is safe to put the queen or not 
    def is_safe(self,row,col,curr_board_config):
        
        for c in range(col):
            if curr_board_config[row][c] == 'Q':
                return False

        # Vertical check to the top only as bottom side is not occupied
        for r in range(row):
            if curr_board_config[r][col] == 'Q':
                return False

        # Top left check
        for c, r in zip(range(col - 1, -1, -1), range(row - 1, -1, -1)):
            if curr_board_config[r][c] == 'Q':
                return False

        # Bottom left check
        for c, r in zip(range(col - 1, -1, -1), range(row + 1, self.N)):
            if curr_board_config[r][c] == 'Q':
                return False

        return True

    # Main function for nqueen probelm
    def solve_n_queens(self):
    
        # helper function to implement recursive call(back-tracking)
        def solve(curr_board_config, col):
            if col >= self.N:
                self.safe_configs.append([''.join(row) for row in curr_board_config])
                return
            for row in range(self.N):
                if self.is_safe(row,col,curr_board_config):
                    curr_board_config[row][col] = 'Q'
                    solve(curr_board_config,col+1)
                    curr_board_config[row][col]='.'
        curr_board_config = self.init_curr_board_config()
        solve(curr_board_config,0)
        return self.safe_configs
def show_safe_states(safe_states):
    i=1
    for safe_state in safe_states:
        print("state:", i)
        for row in safe_state:
            for cell in row:
                print(cell, sep=' ', end= ' ')
            print()
        i+=1
        

if __name__ == "__main__":
    n=4
    # User don't have to change the source code for different values of n.
    # Provide value of n as command line argument.:
    if len(sys.argv) >1:
        n = int(sys.argv[1])

    nqueen = Nqueens(n)
    safe_states = nqueen.solve_n_queens()
    if len(safe_states) == 0:
        print("No solution exists.")
    else:
        show_safe_states(safe_states)
    

        
