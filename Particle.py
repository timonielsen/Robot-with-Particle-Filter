import math
import numpy as np
import random

class Particle:
	def __init__(self, _x, _y, _orientation, ):
		"""initialise the particle"""
		self.x = _x #location
		self.y = _y
		self.sense_noise = 0.0 		# a particle has the same features with robot like moving forward, rotating
		self.rotate_noise = 0.0 	# or measuring distances. Therefore, the noise parameters are added for the simplicity of
		self.forward_noise = 0.0 	# calculations and moving particles.
		self.orientation = _orientation #orientation of particle [0,2PI]
		self.measureMax = 400 #mm - The maximum a robot can measure TODO, make a good way to get this directly from the robot parameters so it's not hardcoded
		self.measureMin = 0 #mm - The minimum a robot can measure TODO, make a good way to get this directly from the robot parameters so it's not hardcoded

		self.rayTracedNodes = {} #This can be deleted later, and is only uses for DEBUGGING. stores the lines of measurements
		""" We can always reevaluate number of points for measurements here. 
		DO NOT MAKE ANY HARD CODED LOOPS AS LENGTH OF ARRAY MAY CHANGE.
		Weight is related to how well the measurements of a particle corresponds with the measurements of a robot. 
		The better match, the higher weight. Note that the resolution has a huge impact on this measure.
		"""

		self.measurements = [0.0,0.0,0.0,0.0,0.0] #calculated distances to nearby walls
		self.manhattanDist = [0.0,0.0,0.0,0.0]
		self.weight = 1.0 #
		self.weight2 = 1.0

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
			raytracer = [float(self.y), float(self.x)] #the raytracer is initialsed at the location of the particle

			intersectionFound = False
			iterator = 0
			while intersectionFound is False:
				#update point on ray which we analyse to see whether it's a wall or not
				raytracer = [raytracer[0] + 0.99*math.cos(angles[k]), raytracer[1] - 0.99*math.sin(angles[k])]
				i = iround(raytracer[0]) #find which cell is in the point we are analysing
				j = iround(raytracer[1])
				self.rayTracedNodes[(i,j)] = (i,j)
				if i < 0 or i > _maze.dimY-1: #if maze dimensions has been exceeded
					nonMetricMeasures.append(-1)
					break

				if j < 0 or j > _maze.dimX-1:#if maze dimensions has been exceeded
					nonMetricMeasures.append(-1)
					break

				if iterator >= maxDist: #if we have reached the maxdist which the robot can measure.
					nonMetricMeasures.append(-1)
					break

				if _maze.fullLayout[i][j] == 1: #if the ray has hit a wall
					distance = pythagoras(self.x - j, self.y-i) #find the distance to the point or impact
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
		self.weight = self.weight / float(_normalisationFactor)
		self.weight2 = self.weight2 / float(_normalisationFactor)
		return 0

	def set_noise(self,_snoise,_fnoise,_rnoise):
		self.sense_noise = _snoise
		self.forward_noise = _fnoise
		self.rotate_noise = _rnoise

	def Gaussian(self, mu, sigma, x):
		return math.exp(-((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))

	def measure_prob(self, robotdist):
		## the measurements of robot and the particle is compared according to sense noise and gaussian dist.
		prob = 1.0
		for i in range(len(self.measurements)):
			prob *= self.Gaussian(self.measurements[i], self.sense_noise, robotdist[i])
		self.weight = prob
		return prob

	def move(self,_angle,_distance,_maze):
		newOr = self.orientation + float(_angle) + 0.2*random.gauss(0.0,(self.rotate_noise/360)*2*math.pi)
		newOr %= 2*math.pi
		self.orientation = newOr
		newdist = float(_distance)
		self.x -= newdist * math.sin(self.orientation)
		self.y += newdist * math.cos(self.orientation)
		if self.x >= _maze.dimX:
			self.x = _maze.dimX-1
		if self.y >= _maze.dimY:
			self.y = _maze.dimY-1
		if self.x < 0:
			self.x = 0.0
		if self.y < 0:
			self.y = 0.0
		return 0


	def getStateofParticle(self):
		return [self.x,self.y,self.orientation]

	def calcDistance2(self,_maze):
		cellx = int(self.x/_maze.resolution)
		celly = int(self.y/_maze.resolution)
		j = cellx
		i = celly
		while _maze.layout[i][j][0] == '0':
			j -= 1
		self.manhattanDist[0] = self.x - (j)*_maze.resolution
		while _maze.layout[i][j][3] == '0':
			j += 1
		self.manhattanDist[2] = (_maze.dimX - self.x-1) - (2-j) * _maze.resolution
		while _maze.layout[i][j][1] == '0':
			i -= 1
		self.manhattanDist[1] = self.y - i * _maze.resolution
		while _maze.layout[i][j][2] == '0':
			i += 1
		self.manhattanDist[3] = (_maze.dimY - self.y-1) - (2 - i) * _maze.resolution
		return 0

	def measure_prob2(self,robotDist):
		prob = [1.0,1.0,1.0,1.0]
		for j in range(len(prob)):
			for i in range(len(robotDist)):
				prob[j] *= self.Gaussian(self.manhattanDist[(j+i)%len(prob)], self.sense_noise, robotDist[i])
		self.weight2 = max(prob)
		return self.weight2

	def add_noise(self,_dimX,_dimY):
		self.x = self.x + random.gauss(0.0, self.forward_noise)
		if self.x >= _dimX:
			self.x = _dimX - 1
		self.y = self.y + random.gauss(0.0, self.forward_noise)
		if self.y >= _dimY:
			self.y = _dimY - 1
		if self.x < 0:
			self.x = 0.0
		if self.y < 0:
			self.y = 0.0
		#self.orientation = (self.orientation + random.gauss(0.0, (self.rotate_noise / 360) * 2 * math.pi)) % (2 * math.pi)

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