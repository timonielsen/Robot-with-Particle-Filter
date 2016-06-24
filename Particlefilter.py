import Particle
import math

class Particlefilter:
	 def __init__(self, _noise, _noOfParticles, _maze):
	 	self.noise = _noise; #the noise with which the resampling of points is affected
	 	self.noOfParticles = _noOfParticles
	 	self.maze = _maze

	 	"""Fill up the particleFilter with randomly placed points.
	 	Somehow we need the dimensions of the maze to do this properly"""
	 	self.particles = []
	 	for i in range(self.noOfParticles):
	 		self.particles.append(Particle.Particle(_maze.dimX/2,_maze.dimY/2,10)) #change to some random value

	 def measure(self):
	 	"""for each particles calculate the distance to the walls"""
	 	for i in range(self.noOfParticles):
	 		self.particles[i].calcDistance(self.maze)
	 		print(self.particles[i].measurements)

	 def compare(self, _robot):
	 	"""compare measurements with measurement of robot and update weights"""
	 	return 0

	 def resample(self):
	 	"""resample particles"""
	 	return 0

	 def updateLocation(self, _robot):
	 	"""move all particles as the robot has moved"""
	 	return 0





'''Class Particlefilter

#variables
float noise;
Particle[] particles;
Robot robot;
Maze maze;
Particlefilter(Maze maze, float noOfParticles); #constructor
'''