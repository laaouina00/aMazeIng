import random
import curses
import time
from collections import deque
from printMaze import build_maze_array, print_maze_curses

class MazeGenerate:

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
            self.solution = False

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = self.mazeGen()

    def mazeGen(self):
        mazz = []
        for row in range(self.height):
            lis = []
            for coll in range(self.width):
                cel = self.Cell(row, coll)
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
        start_col += 4
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


    def bfs(self, start, end):
        q = deque()
        q.append(start)
        visited = {start}
        root = {start: None}
        while q:
            current = q.popleft()
            if current == end:
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = root[node]
                path.reverse()
                for cell in path:
                    cell.solution = True
                return path
            for n in self.where_to_go(current):
                if n not in visited:
                    visited.add(n)
                    root[n] = current
                    q.append(n)
        return []
    

    def add_extra_paths(self, start: tuple, end: tuple) -> None:
    
        for (row, col) in [start, end]:
            cell = self.maze[row][col]
            if row > 0 and not self.maze[row - 1][col].blocked and cell.top:
                cell.top = False
                self.maze[row - 1][col].down = False
            if row < self.height - 1 and not self.maze[row + 1][col].blocked and cell.down:
                cell.down = False
                self.maze[row + 1][col].top = False
            if col > 0 and not self.maze[row][col - 1].blocked and cell.left:
                cell.left = False
                self.maze[row][col - 1].right = False
            if col < self.width - 1 and not self.maze[row][col + 1].blocked and cell.right:
                cell.right = False
                self.maze[row][col + 1].left = False


maze = MazeGenerate(10, 10)
Seed = None
maze.draw_42()
maze.remove_walls(Seed)
maze.add_extra_paths(start=(0, 0), end=(9, 9))
maze_array = build_maze_array(maze)
print_maze_curses(maze, maze_array)