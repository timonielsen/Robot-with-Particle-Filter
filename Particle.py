class Particle:
	def __init__(self, _x, _y, _orientation):
		self.x = _x #location
		self.y = _y
		self.orientation = _orientation #orientation of particle [0,2PI]

		""" We can always reevaluate number of points for measurements here. 
		DO NOT MAKE ANY HARD CODED LOOPS AS LENGTH OF ARRAY MAY CHANGE.

		Weight is related to how well the measurements of a particle corresponds with the measurements of a robot. 
		The better match, the higher weight 
		"""

		self.measurements = [0,0,0,0,0] #calculated distances to nearby walls
		self.weight = 1.0; #

	def calcDistance(_maze):
		"""calculates distance to nearby walls and updates measurements[]"""
		return 0

	def updateLocation(_robot):
		"""Whenever the robot has moved the particles must perform same operation"""
		return 0

	def updateWeight(_robot):
		"""assigns a weight value to the particle based on how well the measurements of the robot fits
		the calculated measurements of the particle"""
		return 0

	def normalizeWeight(_normalisationFactor):
		"""normalises the weight. The normalisation factor will be calculated
		in the particlefilter based after a weight has been assigned to each particle"""
		return 0




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