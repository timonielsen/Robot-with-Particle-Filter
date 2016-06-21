import math

class Particle:
	def __init__(self, _x, _y, _orientation, ):
		"""initialise the particle"""
		self.x = _x #location
		self.y = _y
		self.orientation = _orientation #orientation of particle [0,2PI]
		self.measureMax = 100 #mm - The maximum a robot can measure TODO, make a good way to get this directly from the robot parameters so it's not hardcoded
		self.measureMin = 0 #mm - The minimum a robot can measure TODO, make a good way to get this directly from the robot parameters so it's not hardcoded

		""" We can always reevaluate number of points for measurements here. 
		DO NOT MAKE ANY HARD CODED LOOPS AS LENGTH OF ARRAY MAY CHANGE.
		Weight is related to how well the measurements of a particle corresponds with the measurements of a robot. 
		The better match, the higher weight. Note that the resolution has a huge impact on this measure.
		"""

		self.measurements = [0,0,0,0,0] #calculated distances to nearby walls
		self.weight = 1.0; #

	def calcDistance(self, _maze):
		"""calculates distance to nearby walls and updates measurements[]"""
		"""The function is fairly expensive, so limiting the amount of measures will greatly increase speed"""
		"""CAN THIS BE DONE SMARTER?????"""
		angles = [] #The orientations at which the measurements are carried out
		maxDist = pythagoras(_maze.dimX, _maze.dimY) * 1.1 #A distance greater than the diagonal of the maze doesn't make sense
		#TODO update to whatever distance the robot can actually measure. Maybe somehow get it from the robot class. 

		"""This loop calculates the angles in which the particle will measure"""
		for i in range(0,len(self.measurements)):
			angle = self.orientation + math.pi/2.0 - i * math.pi / (len(self.measurements)-1) # calculates the angles for which the sensors measure
			angle = normalizeAngle(angle)
			angles.append(angle)

		"""The distance the particle measures to the walls is calculated as follows.
		It's assumed a ray is shot out from the particle location [x,y]. We then simply start considering the node
		which the particle is and move  by a distance a little smaller than 1.0 along the 'ray'
		and check what cell we are then in. NOTE: The movement is performed with float and NOT int values.
		It is then checked whether this cell is a wall or not. If it's a wall the euclidian distance to this wall point 
		is calculated. This distance can then be converted to an actual length in cm by taking into account the 
		resolution and cell size of the maze
		Please let me (TIMO) know if this needs further explanation.
		"""

		nonMetricMeasures = [] #Measures in unit lengths
		for k in range(0,len(angles)): #For each angle in which the particle measure
			raytracer = [float(self.x), float(self.y)] #the raytracer is initialsed at the location of the particle

			intersectionFound = False
			iterator = 0
			while intersectionFound is False:
				#update point on ray which we analyse to see whether it's a wall or not
				raytracer = [raytracer[0] - 0.99*math.sin(angles[k]), raytracer[1] + 0.99*math.cos(angles[k])]
				i = iround(raytracer[0]) #find which cell is in the point we are analysing
				j = iround(raytracer[1])
				
				if i < 0 or i > _maze.dimX-1: #if maze dimensions has been exceeded
					nonMetricMeasures.append(-1)
					break

				if j < 0 or j > _maze.dimY-1:#if maze dimensions has been exceeded
					nonMetricMeasures.append(-1)
					break

				if iterator >= maxDist: #if we have reached the maxdist which the robot can measure.
					nonMetricMeasures.append(-1) 
					break

				if _maze.fullLayout[i][j] == 1: #if the ray has hit a wall
					distance = pythagoras(self.x - i, self.y-j) #find the distance to the point or impact
					nonMetricMeasures.append(distance)
					break
				iterator += 1

		#calculate the metric distance to the point which the ray has hit the wall
		for i in range(0, len(nonMetricMeasures)):
			self.measurements[i] = nonMetricMeasures[i] * _maze.fieldsize/_maze.resolution #Checking for division by 0 in initialisation of maze
		return 0

	def updateLocation(self, _robot):
		"""Whenever the robot has moved the particles must perform same operation"""
		return 0

	def updateWeight(self, _robot):
		"""assigns a weight value to the particle based on how well the measurements of the robot fits
		the calculated measurements of the particle"""
		return 0

	def normalizeWeight(self, _normalisationFactor):
		"""normalises the weight. The normalisation factor will be calculated
		in the particlefilter based after a weight has been assigned to each particle"""
		return 0


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
    return newAngle;

def pythagoras(length1, length2):
	"""caulcates the hypothenuse length of a diagonal of a right angled triangle"""
	return math.sqrt(math.pow(length1,2) + math.pow(length2,2))

def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    if x <= 0.5 and x > -0.5:
    	return 0

    return int(round(x) - .5) + (x > 0)


'''Class Particle
#Variables
int x, y;
float orientation;
float[] measurements;
double weight;

#functions
void calcDistance(Maze Maze);
void updateLocation(Robot robot);
void updateWeight(Robot robot);
void normalizeWeight(float n);
'''