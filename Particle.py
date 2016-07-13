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

	def calcDistanceSmarter(self, _maze):
		angles = [] #The orientations at which the measurements are carried out
		maxDist = pythagoras(_maze.dimX, _maze.dimY) * 1.1 #A distance greater than the diagonal of the maze doesn't make sense
		#TODO update to whatever distance the robot can actually measure. Maybe somehow get it from the robot class.

		"""This loop calculates the angles in which the particle will measure"""
		for i in range(0,len(self.measurements)):
			angle = self.orientation + math.pi/2.0 - i * math.pi / (len(self.measurements)-1)			
			angle = normalizeAngle(angle)
			angles.append(angle)

		'''make lines for measurements'''
		lines = []
		for i in range(0,len(angles)):
			lines.append([(float(self.y), float(self.x)), (float(self.y) + 3*maxDist*math.cos(angles[i]), float(self.x) - 3*maxDist*math.sin(angles[i]))])
		nonMetricMeasures = []

		for i in range(0,len(angles)):
			foundIntersection = False
			intersectionDistance = 10000000
			for j in range(0,len(_maze.walls)): 
				#if doIntersect(lines[i][0], lines[i][1], _maze.walls[j][0], _maze.walls[j][1]):
				result = findIntersectionPointbetweenLines(lines[i][0], lines[i][1], _maze.walls[j][0], _maze.walls[j][1])
				#else:
				#	continue
				if result[2] == 0:
					continue
				else:
					foundIntersection = True
				yi = result[0]
				xi = result[1]
				newDist = pythagoras(lines[i][0][0] - yi,lines[i][0][1]-xi)
				if newDist < intersectionDistance:
					intersectionDistance = newDist

			if foundIntersection:
				nonMetricMeasures.append(intersectionDistance)
			else: 
				nonMetricMeasures.append(-1)


		#calculate the metric distance to the point which the ray has hit the wall
		for i in range(0, len(nonMetricMeasures)):
			self.measurements[i] = nonMetricMeasures[i] * _maze.fieldsize/_maze.resolution - 2.0 #Checking for division by 0 in initialisation of maze
		return 0





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
			self.measurements[i] = nonMetricMeasures[i] * _maze.fieldsize/_maze.resolution - 2.0 #Checking for division by 0 in initialisation of maze
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

	def correct(self, _dimX, _dimY, _correctionDistance):
		self.x += _correctionDistance * math.sin(self.orientation)
		self.y -= _correctionDistance * math.cos(self.orientation)
		if self.x >= _dimX:
			self.x = _dimX - 1
		if self.y >= _dimY:
			self.y = _dimY - 1
		if self.x < 0:
			self.x = 0.0
		if self.y < 0:
			self.y = 0.0

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

def pythagoras(length1, length2):
	"""caulcates the hypothenuse length of a diagonal of a right angled triangle"""
	return math.sqrt(math.pow(length1,2) + math.pow(length2,2))

def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    if x <= 0.5 and x > -0.5:
    	return 0

    return int(round(x) - .5) + (x > 0)


# stolen from https://www.cs.hmc.edu/ACM/lectures/intersections.html

def findIntersectionPointbetweenLines( pt1, pt2, ptA, ptB ): 
    """ this returns the intersection of Line(pt1,pt2) and Line(ptA,ptB)
        
        returns a tuple: (xi, yi, valid, r, s), where
        (xi, yi) is the intersection
        r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
        s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
            valid == 0 if there are 0 or inf. intersections (invalid)
            valid == 1 if it has a unique intersection ON the segment    """

    DET_TOLERANCE = 0.00000001

    # the first line is pt1 + r*(pt2-pt1)
    # in component form:
    x1, y1 = pt1;   x2, y2 = pt2
    dx1 = x2 - x1;  dy1 = y2 - y1

    # the second line is ptA + s*(ptB-ptA)
    x, y = ptA;   xB, yB = ptB;
    dx = xB - x;  dy = yB - y;

    # we need to find the (typically unique) values of r and s
    # that will satisfy
    #
    # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
    #
    # which is the same as
    #
    #    [ dx1  -dx ][ r ] = [ x-x1 ]
    #    [ dy1  -dy ][ s ] = [ y-y1 ]
    #
    # whose solution is
    #
    #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
    #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
    #
    # where DET = (-dx1 * dy + dy1 * dx)
    #
    # if DET is too small, they're parallel
    #
    DET = (-dx1 * dy + dy1 * dx)

    if math.fabs(DET) < DET_TOLERANCE: return (0,0,0,0,0)

    # now, the determinant should be OK
    DETinv = 1.0/DET

    # find the scalar amount along the "self" segment
    r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))

    # find the scalar amount along the input line
    s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))

    # return the average of the two descriptions
    xi = (x1 + r*dx1 + x + s*dx)/2.0
    yi = (y1 + r*dy1 + y + s*dy)/2.0
    return ( xi, yi, 1, r, s )




# Given three colinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
       return True
    return False
 
# To find orientation of ordered triplet (p, q, r).
# The function returns following values
# 0 --> p, q and r are colinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p, q, r):
    #See http://www.geeksforgeeks.org/orientation-3-ordered-points/
    #for details of below formula.
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    print(val)
    if val == 0:
    	return 0  # colinear
 	if val > 0:
 		return 1
 	else: 
 		return 2
 
# The main function that returns true if line segment 'p1q1'
# and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    #Find the four orientations needed for general and
    #special cases
    o1 = orientation(p1, q1, p2);
    o2 = orientation(p1, q1, q2);
    o3 = orientation(p2, q2, p1);
    o4 = orientation(p2, q2, q1);
 
    # General case
    if o1 != o2 and o3 != o4:
        return True
 
     #Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if o1 == 0 and onSegment(p1, p2, q1): 
    	return True
 
    #p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if o2 == 0 and onSegment(p1, q2, q1): 
    	return True;
 
    #p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if o3 == 0 and onSegment(p2, p1, q2):
    	return True;
 
     #p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if o4 == 0 and onSegment(p2, q1, q2):
    	return True
 
    return False #// #Doesn't fall in any of the above cases

 
