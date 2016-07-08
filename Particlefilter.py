import Particle
import math
import numpy as np
import turtle
import Robot
import random

class Particlefilter:
	 def __init__(self, _noise, _noOfParticles, _maze):
	 	self.noise = _noise; #the noise with which the resampling of points is affected
	 	self.noOfParticles = _noOfParticles
	 	self.maze = _maze

	 	"""Fill up the particleFilter with randomly placed points.
	 	Somehow we need the dimensions of the maze to do this properly"""
	 	self.particles = []
		self.weights = []
		self.totalWeight = 0 # To normalise the weights of particles
		init_xcoordinates =((_maze.resolution+1) * 3 - 1) * np.random.random_sample(self.noOfParticles,)
		init_ycoordinates = ((_maze.resolution+1) * 3 - 1) * np.random.random_sample(self.noOfParticles,)
		init_angles = 2 * math.pi * np.random.random_sample(self.noOfParticles,)
	 	for i in range(self.noOfParticles):
	 		self.particles.append(Particle.Particle(init_xcoordinates[i],init_ycoordinates[i],init_angles[i])) #change to some random value
			self.particles[i].set_noise(1.0,1.0,5.0)


	 def measure(self):
	 	"""for each particles calculate the distance to the walls"""
	 	for i in range(self.noOfParticles):
	 		self.particles[i].calcDistance(self.maze)

	 		#print(self.particles[i].measurements)



	 def compare(self, _robot):
	 	"""compare measurements with measurement of robot and update weights"""
		robotDistance = _robot.measure()
		self.weights = []
		for p in self.particles:
			p.calcDistance(self.maze)
			self.weights.append(p.measure_prob(robotDistance))
	 	return 0

	 def normalize_weights(self):
		 #print sum(self.weights)
		 self.totalWeight = sum(self.weights)
		 w1 = []
		 for p in self.particles:
			 p.normalizeWeight(self.totalWeight)
			 w1.append(p.weight)
		 self.weights = w1

	 def resample(self):
	 	"""resample particles"""
		## for resampling, a roulette wheel implementaion used.
		## http://ais.informatik.uni-freiburg.de/teaching/ss11/robotics/slides/11-pf-mcl.ppt.pdf
		resampledparticles = []
		index = int(np.random.uniform()*self.noOfParticles)
		maxW = max(self.weights)
		beta = 0.0
		for i in range(self.noOfParticles):
			beta = beta + np.random.uniform()*2*maxW
			while self.particles[index].weight < beta:
				beta = beta - self.particles[index].weight
				index = (index+1)%self.noOfParticles
			resampledparticles.append(self.particles[index])
		self.particles = []
		self.particles = resampledparticles
		#print resampledparticles[5].x
	 	return 0

	 def updateLocation(self, _angle,_distance):
	  	"""move all particles as the robot has moved"""
		for p in self.particles:
			p.move(_angle,_distance,self.maze)
	 	return 0

	 def showParticles(self, _loc):
		 turtle.tracer(50000, delay=0)
		 turtle.register_shape("dot", ((-3, -3), (-3, 3), (3, 3), (3, -3)))
		 turtle.register_shape("tri", ((-3, -2), (0, 3), (3, -2), (0, 0)))
		 turtle.speed(0)
		 turtle.setworldcoordinates(0,(self.maze.resolution+1)*3,(self.maze.resolution+1)*3,0)
		 turtle.up()
		 turtle.clearstamps()
		 turtle.shape('tri')
		 print len(self.particles)
		 for p in self.particles:
			 #print(p.x,p.y)
			 p.x = p.x + random.gauss(0.0,p.forward_noise)
			 p.y = p.y + random.gauss(0.0, p.forward_noise)
			 turtle.setposition(p.x,p.y)
			 heading = (p.orientation/(2*math.pi))*360
			 turtle.setheading(heading)
			 turtle.color("red")
			 turtle.stamp()
			 #turtle.update()
		 turtle.shape('turtle')
		 turtle.color("green")
		 turtle.setposition(_loc[0],_loc[1])
		 headingr = (_loc[2]/(2*math.pi))*360
		 turtle.setheading(headingr)
		 turtle.update()











'''Class Particlefilter

#variables
float noise;
Particle[] particles;
Robot robot;
Maze maze;
Particlefilter(Maze maze, float noOfParticles); #constructor
'''