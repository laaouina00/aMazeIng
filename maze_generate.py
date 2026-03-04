class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {
            "top" : True,
            "right" : True,
            "down" : True,
            "left" : True
        }
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

    def where_to_go(self):
        pass

    def remove_walls(self):
        pass





def PrintMaze(maz):
    for row in maz.maze:
        for cel in row:
            print("+", end=" ")
        print()

mazee = MazeGenerate(13, 13)
PrintMaze(mazee)


