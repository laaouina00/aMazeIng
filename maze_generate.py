import random
import curses
import time

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.top = True
        self.right = True
        self.down = True
        self.left = True
        self.blocked = False
        self.visited = False


class MazeGenerate:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = self.mazeGen()

    def mazeGen(self):
        mazz = []
        for row in range(self.height):
            lis = []
            for coll in range(self.width):
                cel = Cell(row, coll)
                lis.append(cel)
            mazz.append(lis)
        return mazz

    def draw_42(self):
        center_row = self.height // 2
        center_col = self.width // 2
        start_row = center_row - 3
        start_col = center_col - 3
        for i in range(3):
            self.maze[start_row + i][start_col].blocked = True
        for i in range(3):
            self.maze[start_row + 2][start_col + i].blocked = True
        for j in range(3):
            self.maze[start_row + 2 + j][start_col + 2].blocked = True
        start_col += 3
        for j in range(3):
            self.maze[start_row][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row + j][start_col + 2].blocked = True
        for j in range(3):
            self.maze[start_row + 2][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row + 4][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row + 2 + j][start_col].blocked = True
    
    def where_to_go(self, cell):

        neighbors = []
        row = cell.row
        col = cell.col
        if row > 0 and not cell.blocked:
            neighbors.append(self.maze[row - 1][col])
        if row < self.height - 1 and not cell.blocked:
            neighbors.append(self.maze[row + 1][col])
        if col > 0 and not cell.blocked:
            neighbors.append(self.maze[row][col - 1])
        if col < self.width - 1 and not cell.blocked:
            neighbors.append(self.maze[row][col + 1])

        return neighbors

    def remove_walls(self, Seed):
        #callback
        random.seed(Seed)
        start_row = random.randrange(0, self.height)
        start_col = random.randrange(0, self.width)
        current_cell = self.maze[0][0]
        current_cell.visited = True
        stack = [current_cell]
        while stack:
            current_cell = stack[-1]
            next_cell = self.where_to_go(current_cell)
            unvisited = [cel for cel in next_cell if not cel.visited and not cel.blocked]
            if unvisited:
                next_cell = random.choice(unvisited)
                if next_cell.row < current_cell.row:
                    current_cell.top = False
                    next_cell.down = False
                elif next_cell.row > current_cell.row:
                    current_cell.down = False
                    next_cell.top = False
                elif next_cell.col < current_cell.col:
                    current_cell.left = False
                    next_cell.right = False
                elif next_cell.col > current_cell.col:
                    current_cell.right = False
                    next_cell.left = False
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
        



def build_maze_array(maz):
    height = maz.height
    width = maz.width
    maze_array = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]
    for r in range(height):
        for c in range(width):
            cell = maz.maze[r][c]
            maze_r = r * 2 + 1
            maze_c = c * 2 + 1
            maze_array[maze_r][maze_c] = 0
            if not cell.right and c < width - 1:
                maze_array[maze_r][maze_c + 1] = 0
            if not cell.down and r < height - 1:
                maze_array[maze_r + 1][maze_c] = 0
    maze_array[1][0] = 0
    maze_array[height * 2 - 1][width * 2] = 0
    return maze_array



def print_maze_curses(maze_array):
    def draw(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        for r, row in enumerate(maze_array):
            for c, val in enumerate(row):
                if val == 1:
                    stdscr.addstr(r, c, "█", curses.color_pair(1))
                elif val == 0:
                    stdscr.addstr(r, c, " ", curses.color_pair(2))
                # time.sleep(0.001)
        stdscr.refresh()
        stdscr.getch()
    curses.wrapper(draw)


maze = MazeGenerate(20, 20)
Seed = None
maze.draw_42()
maze.remove_walls(Seed)
maze_array = build_maze_array(maze)
print_maze_curses(maze_array)