from operator import itemgetter
try:
    # for Python2
    import Tkinter as tk   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    import tkinter as tk   ## notice here too
import math


class Maze:
    def __init__(self, _layout, _resolution, _fieldsize):
        """Initiliases the maze"""
        if _resolution <= 0 or _fieldsize <= 0 or _layout == 0:
            print("Error in maze input")
            exit()

        #Maze geoemtry and layout
        self.layout = _layout #Simple layout of maze, which is translated into a full layout
        self.resolution = _resolution #Resolution with which the full layout will be produced
        self.fieldsize = _fieldsize #Size of each cell in maze. In the competetion case is 30 (cm)
        self.cellSize = float(_fieldsize)/float(_resolution)

        #Refinement of layout
        self.fullLayout = self.layoutMaker()

        #Refinement of node data
        self.allNodes = {} #Nodes of the maze containieng all info of each node. # [y, x, wall, fcost(total), hcost (heueristic), gcost (movement), parent, weight]
        self.target = {} #Exit field
        self.dimX = len(self.fullLayout[0]) #Dimension of grid in X direction
        self.dimY = len(self.fullLayout) #Dimension of grid in Y direction
        self.wallCoor = []

        #Parameters for path finding
        self.home = (0, 0) #Location of robot.
        self.openList = []
        self.closedList = []
        self.check = []
        self.path = [] #The path from location of robot to the exit
        self.nodeSetup()

    def layoutMaker(self):
        """ Buid a layout from a very simple layout. The layout must be rectangular!!!
        Each cell is a four char string where each char tells wether there is a wall next to cell.
        The count is Left-Up-Down-Right. EG. XXOO is a cell with walls to at left and up. E is a reference to where the exit is:

        layout = [['XXOO', 'OXXO', 'OXXX'],
                  ['XOXO', 'OXXO', 'OXOX'],
                  ['XXXO', 'OXXO', 'OOEX']]
        looks like:
        _______
        |  ____|
        |____  |
        |____  |
        """

        # Cheack that the layout is legit
        for i in range(0, len(self.layout)):
            for j in range(0, len(self.layout[i])):
                """In this loop it is checked that the maze is sorrounded by walls, expect for where
                there are opening. It is also checked that the value of nieghbour cells correspond to each other.
                A cell A = [...X] must have a right neighboor B=[X...]
                """
                errormessage1 = "cell (" + str(i) + ", " + str(j) + ") is an edge cell but is open"
                errormessage2 = "cell (" + str(i) + ", " + str(j) + ") has an error with the cell in direction: "

                checkLeft = True
                checkUp = True
                checkDown = True
                checkRight = True

                # check that the maze is closed
                if i == 0:  # Considering the top row of cells
                    checkUp = False  # Obviously doesn't make sense to check with cells above the top row
                    if self.layout[i][j][1] == 'O':
                        print(errormessage1)
                        exit()

                if i == len(self.layout) - 1:  # Considering the bottom row of cells
                    checkDown = False
                    if self.layout[i][j][2] == 'O':
                        print(errormessage1)
                        exit()

                if j == 0:  # Considering the left row of cells
                    checkLeft = False
                    if self.layout[i][j][0] == 'O':
                        print(errormessage1)
                        exit()

                if j == len(self.layout[i]) - 1:  # Considering the right row of cells
                    checkRight = False
                    if self.layout[i][j][3] == 'O':
                        print(errormessage1)
                        exit()

                # Check if neighbours have same values (such that a wall/opening is defined from both sides)
                if checkUp:
                    if self.layout[i][j][1] != self.layout[i - 1][j][2]:
                        print(errormessage2 + "UP")
                        exit()

                if checkDown:
                    if self.layout[i][j][2] != self.layout[i + 1][j][1]:
                        print(errormessage2 + "DOWN")
                        exit()

                if checkLeft:
                    if self.layout[i][j][0] != self.layout[i][j - 1][3]:
                        print(errormessage2 + "LEFT")
                        exit()

                if checkRight:
                    if self.layout[i][j][3] != self.layout[i][j + 1][0]:
                        print(errormessage2 + "RIGHT")
                        exit()

        # Now build the full layout. Don't worry too much about this part. It's a bit of a goose chase
        # to really understand the matrix operations without drawing what is actually happening
        fullLayoutCellBased = [];  # First the individual cells are scaled and this will then afterwards.

        # For each cell
        for i in range(0, len(self.layout)):
            layoutRow = []
            for j in range(0, len(self.layout[i])):
                cell = []

                # create a matrix of size res x res for each cell
                for m in range(0, self.resolution):
                    cellRow = []
                    for n in range(0, self.resolution):
                        makeWall = False
                        makeExit = False
                        if n == 0:
                            if self.layout[i][j][0] == 'X':
                                makeWall = True
                            elif self.layout[i][j][0] == 'E' and m == self.resolution / 2:
                                makeExit = True

                        if n == self.resolution - 1:
                            if self.layout[i][j][3] == 'X':
                                makeWall = True
                            elif self.layout[i][j][3] == 'E' and m == self.resolution / 2:
                                makeExit = True

                        if m == 0:
                            if self.layout[i][j][1] == 'X':
                                makeWall = True
                            elif self.layout[i][j][1] == 'E' and n == self.resolution / 2:
                                makeExit = True

                        if m == self.resolution - 1:
                            if self.layout[i][j][2] == 'X':
                                makeWall = True
                            elif self.layout[i][j][2] == 'E' and n == self.resolution / 2:
                                makeExit = True

                        if makeExit:
                            cellRow.append(2)
                        elif makeWall:
                            cellRow.append(1)
                        else:
                            cellRow.append(0)
                    cell.append(cellRow)
                layoutRow.append(cell)
            fullLayoutCellBased.append(layoutRow)
        fullLayout = [];

        # Put together the maze to one single matrix
        for i in range(0, len(fullLayoutCellBased)):
            for m in range(0, len(fullLayoutCellBased[i][0])):
                fullLayoutRow = []
                for j in range(0, len(fullLayoutCellBased[i])):
                    for n in range(0, len(fullLayoutCellBased[i][j][m])):
                        fullLayoutRow.append(fullLayoutCellBased[i][j][m][n])
                fullLayout.append(fullLayoutRow)
        return fullLayout

    def nodeSetup(self):

        # self.fullLayout = self.layoutMaker()
        sizeX = self.dimX #TODO: Explain what is 3?
        sizeY = self.dimY

        # converting maze array into nodes with cost values and locations
        for u in range(0, sizeY):
            for v in range(0, sizeX):

                # [y, x, wall, fcost(total), hcost (heueristic), gcost (movement), parent, weight]
                self.allNodes[(u, v)] = [u, v, self.fullLayout[u][v], 10000, 0, 0, (0, 0), 0]

                # selecting the target node from array
                if self.fullLayout[u][v] == 2:
                    self.target = self.allNodes[(u, v)]

        # Assigning weights to the node that are close to the walls
        for a in range(0, sizeY):
            for b in range(0, sizeX):

                if self.fullLayout[a][b] == 1:
                    directions_w = [[1, 0], [0, 1], [-1, 0], [0, -1]]#, [-1, -1], [1, -1], [-1, 1], [1, 1]]

                    for dirW in directions_w:
                        for d in range(1, int(self.resolution / 2)):
                            weight = self.resolution*1000 / d
                            if 0 < (a + dirW[0] * d) < (sizeY) and 0 < (b + dirW[1] * d) < (sizeX) \
                                    and self.allNodes[(a + dirW[0] * d, b + dirW[1] * d)][7] < weight:

                                self.allNodes[(a + dirW[0] * d, b + dirW[1] * d)][7] = weight

        # starting the open and closed list for A*
        self.openList = [self.allNodes[self.home]]
        self.closedList = []

    def neighbors(self, node):
        # Directions to the neighbors of the selected node
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]#, [-1, -1], [1, -1], [-1, 1], [1, 1]]

        # Empty list for the real neighbors that are inside the maze and are not walls with updated cost values
        realNeighbor = []
        d = 0

        for dir in directions:
            d += 1
            nodeX = node[0] + dir[0]
            nodeY = node[1] + dir[1]
            neighbor = (nodeX, nodeY)
            tcost = 1000

            ''' if the neighboring node is inside the maze and not a wall and the nodes
                is either unexplored or the new route to the node is cheaper than the existing'''
            if neighbor in self.allNodes and self.allNodes[neighbor][2] != 1:

                if (node[1] - self.allNodes[tuple(node)][6][1]) * neighbor[0] + \
                                (self.allNodes[tuple(node)][6][1] - neighbor[1]) * node[0] + \
                                (neighbor[1] - node[1]) * self.allNodes[tuple(node)][6][0] == 0:

                    tcost = 0

                if d < 5:
                    # Adding 10 movement cost for straights moves + node weight
                    g = self.allNodes[tuple(node)][5] + 10 + self.allNodes[neighbor][7] + tcost

                if d > 4:
                    # Adding 14 movement cost for diagonal moves + node weight
                    g = self.allNodes[tuple(node)][5] + 14 + self.allNodes[neighbor][7] + tcost

                if self.allNodes[neighbor][6] == (0, 0) or g < self.allNodes[neighbor][5]:

                    # update node withe new weights and parents
                    self.allNodes[neighbor][4] = (round(math.hypot(self.target[0] - neighbor[0],
                                                                   self.target[1] - neighbor[1])) * 10)
                    self.allNodes[neighbor][5] = g
                    self.allNodes[neighbor][3] = self.allNodes[neighbor][4] + g
                    self.allNodes[neighbor][6] = node
                    realNeighbor.append(self.allNodes[neighbor])

        return realNeighbor


    def astar(self):
        while self.openList:

            # sorting the open list of nodes to explore with least fcost then least hcost being sorted to the front
            self.openList = sorted(self.openList, key=itemgetter(3, 4))

            # selecting the first node in the list to check
            self.check = [self.openList[0][0], self.openList[0][1]]

            # deleting selected node from open list
            del self.openList[0]

            # checking selected node for neighbors
            newNeighbor = self.neighbors(self.check)

            # checking if any one of the new neighbors is the target
            for n in newNeighbor:

                # if the neighbor is the target then stop the algorithm and print the path to it
                if [n[0], n[1]] == [self.target[0], self.target[1]]:
                    print('Path Found')
                    path = self.getPath(n)
                    return

                # else add the new neighbors to the open list
                else:
                    self.openList.append(n)

            # adding the checked node to the closed nodes list
            self.closedList.append(self.check)

        print('No Path found')

    def update(self, _loc):
        self.home = _loc
        self.openList = [self.allNodes[self.home]]
        self.closedList = []
        self.path = []
        self.nodeSetup()

    def getPath(self, finish):
        """Finding the path from the target to the starting node by going back through the parents of each node"""

        parent = tuple([finish[0], finish[1]])
        while True:
            if parent != self.home:
                self.path.append(parent)
                parent = tuple(self.allNodes[parent][6])

            else:
                return self.path
    def printPath(self):
        print(self.path)

    def printLayoutAdvanced(self, _type):
        """prints the layout with more infomation, good for debugging.
        Each field is printed as F_XXX_YYY where F is a reference to the function of the cell and
        XXX is the Z cordinate and YYY is Y coordinate counting from upper left corner
        type = 0: prints regular layour
        type = 1: Prints function of cell as well as coordinate
        type = 2: As type 0 but with path drawn
        type = 3: Prints weights of fields"""

        if self.fullLayout == 0:
            return 0

        if _type==0:
            self.printLayout()
            return 0

        if _type==1:
            if self.dimX > 999 or self.dimY >999:
                print("Dimensions of maze too large for advanced print of layout")
                return 0
            print('')
            for i in range(0,len(self.fullLayout)):
                printRow = []
                for j in range(0,len(self.fullLayout[i])):
                    printRow.append(str(self.fullLayout[i][j]) + '_' + format(i,'03d') +'_'+ format(j,'03d'))
                print(" ".join(printRow))
                print('')
                print('')
            return 0

        if _type==2:
            for i in range(0,len(self.fullLayout)):
                printRow = []
                for j in range(0, len(self.fullLayout[i])):
                    element = ' '
                    if self.fullLayout[i][j] == 0:
                        element = ' '
                    elif self.fullLayout[i][j] == 1:
                        element = 'X'
                    else:
                        element = 'O'
                    if (i,j) in self.path:
                        element = '*'
                    printRow.append(element)
                " ".join(printRow)
                print(" ".join(printRow))

        if _type==3:
            for i in range(0,len(self.fullLayout)):
                printRow = []
                for j in range(0,len(self.fullLayout[i])):
                    printRow.append(format(self.allNodes[(i,j)][7],'05d'))
                print(" ".join(printRow))
                print('')
        return 0

    def printLayoutAdvancedParticleFilter(self, _particlefilter, _type):
        """Prints the particles with or without the lines of measurements.
        type = 4: Without lines
        type = 5: with lines
        """
        if _type == 4:
            for i in range(0,len(self.fullLayout)):
                printRow = []
                for j in range(0, len(self.fullLayout[i])):
                    element = ' '
                    if self.fullLayout[i][j] == 0:
                        element = ' '
                    elif self.fullLayout[i][j] == 1:
                        element = 'X'
                    else:
                        element = 'O'
                    for particle in _particlefilter.particles:
                        if i == int(round(particle.y)) and j == int(round(particle.x)):
                            element = 'P'
                    printRow.append(element)
                " ".join(printRow)
                print(" ".join(printRow))

        if _type == 5:
            for i in range(0,len(self.fullLayout)):
                printRow = []
                for j in range(0, len(self.fullLayout[i])):
                    element = ' '
                    if self.fullLayout[i][j] == 0:
                        element = ' '
                    elif self.fullLayout[i][j] == 1:
                        element = 'X'
                    else:
                        element = 'O'
                    for particle in _particlefilter.particles:
                        if i == int(round(particle.y)) and j == int(round(particle.x)):
                            element = 'P'
                        if (i,j) in particle.rayTracedNodes and self.fullLayout[i][j] != 1:
                            element = '*'
                    printRow.append(element)
                " ".join(printRow)
                print(" ".join(printRow))

    def printLayoutAdvancedRobot(self, _robot, _type):
        """Prints the particles with or without the lines of measurements.
        type = 6: measurelines of robot
        """

        if _type == 6:
            for i in range(0,len(self.fullLayout)):
                printRow = []
                for j in range(0, len(self.fullLayout[i])):
                    element = ' '
                    if self.fullLayout[i][j] == 0:
                        element = ' '
                    elif self.fullLayout[i][j] == 1:
                        element = 'X'
                    else:
                        element = 'O'
                    if i == int(round(_robot.pr.y)) and j == int(round(_robot.pr.x)):
                        element = 'P'
                    if (i,j) in _robot.pr.rayTracedNodes and self.fullLayout[i][j] != 1:
                        element = '*'
                    printRow.append(element)
                " ".join(printRow)
                print(" ".join(printRow))






    def printLayout(self):
        """prints the maze in the console"""
        if self.fullLayout == 0:
            return 0

        for row in self.fullLayout:
            printRow = []
            for el in row:
                if el == 0:
                    printRow.append(' ')
                elif el == 1:
                    printRow.append('X')
                else:
                    printRow.append('O')
            " ".join(printRow)
            print(" ".join(printRow))



def normalizeAngle(angle):
    newAngle = angle
    iterator = 0

    while (newAngle < 0):
        newAngle += 2*math.pi
        iterator += 1
        if iterator > 1000000:
            print("An angle calculation in DEF normalizeAngle went wrong. Input angle was " + int(angle))
            exit()
    while (newAngle >= 2*math.pi):
        newAngle -= 2*math.pi
        iterator += 1
        if iterator > 1000000:
            print("An angle calculation in DEF normalizeAngle went wrong. Input angle was " + int(angle))
            exit()
    return newAngle


'''
start = (23, 2)
resolution = 8
fieldsize = 1
layout = [['XXOO', 'OXXO', 'OXXX'],
	      ['XOXO', 'OXOO', 'OXXX'],
	      ['XXXO', 'OOXO', 'OXEX']]

newMaze = Maze(layout, resolution, fieldsize)
newMaze.astar()


# Figure Drawing

mazeWalls1 = [[90, 90], [240, 90]]
mazeWalls2 = [[10, 160], [90, 160]]
mazeWalls3 = [[160, 160], [240, 160]]

mazeWalls4 = [[10, 10], [240, 10]]
mazeWalls5 = [[240, 10], [240, 240]]
mazeWalls6 = [[160, 240], [10, 240]]
mazeWalls7 = [[10, 240], [10, 10]]

pathD = newMaze.path
pathD.append(start)

path2 = []
for y in pathD:
    path2 += [[x * 10 for x in y]]

root = tk.Tk()
root.geometry("460x460")
root.title("Drawing lines to a canvas")

cv = tk.Canvas(root, height="460", width="460", bg="white")
cv.pack()


def linemaker(screen_points):
    """ Function to take list of points and make them into lines
    """
    is_first = True
    # Set up some variables to hold x,y coods
    x0 = y0 = 0
    # Grab each pair of points from the input list
    for (x, y) in screen_points:
        # If its the first point in a set, set x0,y0 to the values
        if is_first:
            x0 = x
            y0 = y
            is_first = False
        else:
            # If its not the fist point yeild previous pair and current pair
            yield x0, y0, x, y
            # Set current x,y to start coords of next line
            x0, y0 = x, y


list_of_screen_coods = path2

for (x0, y0, x1, y1) in linemaker(list_of_screen_coods):
    cv.create_line(x0, y0, x1, y1, width=1, fill="red")

for (x0, y0, x1, y1) in linemaker(mazeWalls1):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

for (x0, y0, x1, y1) in linemaker(mazeWalls2):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

for (x0, y0, x1, y1) in linemaker(mazeWalls3):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

for (x0, y0, x1, y1) in linemaker(mazeWalls4):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

for (x0, y0, x1, y1) in linemaker(mazeWalls5):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

for (x0, y0, x1, y1) in linemaker(mazeWalls6):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

for (x0, y0, x1, y1) in linemaker(mazeWalls7):
    cv.create_line(x0, y0, x1, y1, width=1, fill="black")

root.mainloop()
'''
