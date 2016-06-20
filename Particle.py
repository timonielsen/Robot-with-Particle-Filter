import math

class Particle:
	def __init__(self, _x, _y, _orientation, ):
		self.x = _x #location
		self.y = _y
		self.orientation = _orientation #orientation of particle [0,2PI]
		self.measureMax = 100 #mm - The maximum a robot can measure TODO, make a good way to get this directly from the robot parameters so it's not hardcoded
		self.measureMin = 0 #mm - The minimum a robot can measure TODO, make a good way to get this directly from the robot parameters so it's not hardcoded

		""" We can always reevaluate number of points for measurements here. 
		DO NOT MAKE ANY HARD CODED LOOPS AS LENGTH OF ARRAY MAY CHANGE.

		Weight is related to how well the measurements of a particle corresponds with the measurements of a robot. 
		The better match, the higher weight 
		"""

		self.measurements = [0,0,0,0,0] #calculated distances to nearby walls
		self.weight = 1.0; #

	def calcDistance(self, _maze):
		"""calculates distance to nearby walls and updates measurements[]"""
		angles = []
		maxDist = pythagoras(_maze.dimX, _maze.dimY) * 1.1 #A distance greater than the diagonal of the maze doesn't make sense
		
		for i in range(0,len(self.measurements)):
			angle = self.orientation - math.pi/2.0 + i * math.pi / (len(self.measurements)-1) # calculates the angles for which the sensors measure
			angle = normalizeAngle(angle)
			angles.append(angle)

		"""The distance the particle measures to the walls is calculated as follows.
		It's assumed a ray is shot out from the particle location [x,y]. We then simply move out
		that 'ray' by a distance a little smaller than 1.0 and check what cell we are then in.
		It is then checked whether this cell is a wall or not. If it's a wall the euclidian distance to this wall point 
		is calculated. This distance can then be converted to an actual length in cm by taking into account the 
		resolution and cell size of the maze"""

		for i in range(0,len(angles)):
			nonMetricMeasures = [] #Measures in unit lengths

			raytracer = [float(self.x), float(self.y)] #the raytracer be
			intersectionFound = False
			iterator = 0
			while intersectionFound is False:
				g = 0
				raytracer = [raytracer[0] + 0.99*math.cos(angles[i]), raytracer[1] + 0.99*math.sin(angles[i])]

				i = iround(raytracer[0])
				j = iround(raytracer[1])

				if i < 0 or i > _maze.dimX:
					nonMetricMeasures.append(-1)
					break

				if j < 0 or j > _maze.dimY:
					nonMetricMeasures.append(-1)
					break

				if iterator >= maxDist:
					nonMetricMeasures.append(-1)
					break

				if _maze.fullLayout[i][j] == 1: #if the ray has hit a wall
					distance = pythagoras(self.x - i, self.y-j)
					nonMetricMeasures.append(distance)

				iterator += 1

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
    		print("An angle calculation in DEF normalizeAngle went wrong. Inpu angle was " + int(angle))
    		exit()
    while (newAngle >= 2*math.pi):
    	newAngle -= 2*math.pi
     	iterator += 1
    	if iterator > 1000000:
    		print("An angle calculation in DEF normalizeAngle went wrong. Inpu angle was " + int(angle))
    		exit()
    return newAngle;

def pythagoras(length1, length2):
	"""caulcates the hypothenuse length of a diagonal of a right angled triangle"""
	return math.sqrt(math.pow(length1,2) + math.pow(length2,2))

def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
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