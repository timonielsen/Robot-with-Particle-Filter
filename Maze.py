class Maze:
	def __init__(self, _layout, _home):
		self.layout = _layout
		self.home = _home
		self.allnodes = 0


	def layoutMaker(self, _layout ,_resolution, _fieldsize):
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

		#Cheack that the layout is legit
		for i in range(0, len(_layout)):
			for j in range(0,len(_layout[i])):
				"""In this loop it is checked that the maze is sorrounded by walls, expect for where
				there are opening. It is also checked that the value of nieghbour cells correspond to each other.
				A cell A = [...X] must have a right neighboor B=[X...] 
				"""
				errormessage1 = "cell (" + str(i) + ", " + str(j) +") is an edge cell but is open"
				errormessage2 = "cell (" + str(i) + ", " + str(j) +") has an error with the cell in direction: "

				checkLeft  = True
				checkUp    = True
				checkDown  = True
				checkRight = True

				#check that the maze is closed 
				if i == 0: 								#Considering the top row of cells
					checkUp = False 					#Obviously doesn't make sense to check with cells above the top row
					if _layout[i][j][1] == 'O':
						print(errormessage1)
						exit()

				if i == len(_layout)-1: 				#Considering the bottom row of cells
					checkDown = False 			
					if _layout[i][j][2] == 'O':
						print(errormessage1)
						exit()

				if j == 0: 								#Considering the left row of cells
					checkLeft = False 			
					if _layout[i][j][0] == 'O':
						print(errormessage1)
						exit()

				if j == len(_layout[i])-1: 				#Considering the right row of cells
					checkRight = False 			
					if _layout[i][j][3] == 'O':
						print(errormessage1)
						exit()

				#Check if neighbours have same values (such that a wall/opening is defined from both sides)
				if checkUp:
					if _layout[i][j][1] != _layout[i-1][j][2]:
						print(errormessage2 + "UP")
						exit()

				if checkDown:
					if _layout[i][j][2] != _layout[i+1][j][1]:
						print(errormessage2 + "DOWN")
						exit()

				if checkLeft:
					if _layout[i][j][0] != _layout[i][j-1][3]:
						print(errormessage2 + "LEFT")
						exit()

				if checkRight:
					if _layout[i][j][3] != _layout[i][j+1][0]:
						print(errormessage2 + "RIGHT")
						exit()

		#Now build the full layout. Don't worry too much about this part. It's a bit of a goose chase
		#to really understand the matrix operations without drawing something
		fullLayoutCellBased = []; #First the individual cells are scaled and this will then afterwards.
		for i in range(0, len(_layout)):
			layoutRow = []
			for j in range(0,len(_layout[i])):
				cell = []

				for m in range(0,_resolution):
					cellRow = []
					for n in range(0,_resolution):
						if   n == 0             and _layout[i][j][0] == 'X':
							makeWall = True
						elif n == _resolution-1 and _layout[i][j][3] == 'X':
							makeWall = True
						elif m == 0             and _layout[i][j][1] == 'X':
							makeWall = True
						elif m == _resolution-1 and _layout[i][j][2] == 'X':
							makeWall = True
						else:
							makeWall = False

						if makeWall:
							cellRow.append('1')
						else:
							cellRow.append('0')
					cell.append(cellRow)
				layoutRow.append(cell)
			fullLayoutCellBased.append(layoutRow)
		fullLayout = [];

		#Put together the maze to one single matrix
		for i in range(0,len(fullLayoutCellBased)):
			for m in range(0,len(fullLayoutCellBased[i][0])):
				fullLayoutRow = []
				for j in range(0,len(fullLayoutCellBased[i])):
					for n in range(0,len(fullLayoutCellBased[i][j][m])):
						fullLayoutRow.append(fullLayoutCellBased[i][j][m][n])
				fullLayout.append(fullLayoutRow)
				print(fullLayoutRow)



'''Class Maze

int[] layout; ##would it be smart to make as a int[][]?
int[][] home;
struct allNodes;

void Maze(int[] layout, [][]) #constructor
'''