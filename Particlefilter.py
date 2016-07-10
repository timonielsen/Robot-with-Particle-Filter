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
		self.offset = 10 #distance from the walls
	 	"""Fill up the particleFilter with randomly placed points.
	 	Somehow we need the dimensions of the maze to do this properly"""
	 	self.particles = []
		self.weights = []
		self.totalWeight = 0 # To normalise the weights of particles
		self.prWithHeighestW = 0
		firstrowParticles = int(self.noOfParticles/3)
		secondrowParticles = self.noOfParticles - 2*firstrowParticles
		thirdrowParticles = self.noOfParticles - secondrowParticles - firstrowParticles
		interval = _maze.resolution - 2*self.offset - 1
		y1 = [x + self.offset for x in interval * np.random.random_sample(firstrowParticles,)]
		y2 = [x + self.offset + _maze.resolution for x in interval * np.random.random_sample(secondrowParticles,)]
		y3 = [x + self.offset + 2*_maze.resolution for x in interval * np.random.random_sample(thirdrowParticles,)]
		init_ycoordinates = y1+y2+y3
		init_xcoordinates = (self.maze.resolution*3-1-2*self.offset)*np.random.random_sample(self.noOfParticles,)
		init_xcoordinates = [x+self.offset for x in init_xcoordinates]
		init_angles = 2 * math.pi * np.random.random_sample(self.noOfParticles,)
	 	for i in range(self.noOfParticles):
	 		self.particles.append(Particle.Particle(init_xcoordinates[i],init_ycoordinates[i],init_angles[i])) #change to some random value
			self.particles[i].set_noise(5.0,1.0,1.0)

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
		maxV = 0.0
		indexOfMaxV = 0
		for i in range(self.noOfParticles):
			if (i%10)== 0 :
				index2 = int(np.random.uniform() * self.noOfParticles)
				resampledparticles.append(Particle.Particle(self.particles[index2].x, self.particles[index2].y,self.particles[index2].orientation))
				resampledparticles[i].set_noise(5.0, 1.0, 1.0)
			else:
				beta = beta + np.random.uniform()*2*maxW
				while self.particles[index].weight < beta:
					beta = beta - self.particles[index].weight
					index = (index+1)%self.noOfParticles
				resampledparticles.append(Particle.Particle(self.particles[index].x,self.particles[index].y,self.particles[index].orientation))
				resampledparticles[i].set_noise(5.0,1.0,1.0)
				if(self.particles[index].weight>maxW):
					maxW = self.particles[index].weight
					indexOfMaxV = i
		self.particles = []
		self.particles = resampledparticles
		self.prWithHeighestW = indexOfMaxV
		#print resampledparticles[5].x
		#print self.particles[5].x
	 	#return 0

	 def reset_particles(self):
		 for p in self.particles:
			 p.weight = 0.0
			 p.measurements = [0.0,0.0,0.0]

	 def updateLocation(self, _angle,_distance):
	  	"""move all particles as the robot has moved"""
		for i in range(0, self.noOfParticles):
			self.particles[i].move(_angle,_distance,self.maze)
	 	return 0

	 def showParticles(self, _loc):
		 turtle.tracer(50000, delay=0)
		 turtle.register_shape("dot", ((-3, -3), (-3, 3), (3, 3), (3, -3)))
		 turtle.register_shape("tri", ((-3, -2), (0, 3), (3, -2), (0, 0)))
		 turtle.speed(0)
		 turtle.setworldcoordinates(0,(self.maze.resolution+1)*3,(self.maze.resolution+1)*3,0)
		 turtle.up()
		 turtle.clearstamps()
		 lines = turtle.Turtle()
		 lines.color("black")
		 lines.pensize(5)
		 for i in range(len(self.maze.layout)):
			 for j in range(len(self.maze.layout[0])):
				 if self.maze.layout[i][j][2]=='X':
					 lines.penup()
					 lines.goto(j*(self.maze.resolution)-1,(i+1)*self.maze.resolution-1)
					 lines.pendown()
					 lines.forward(self.maze.resolution)
					 lines.penup()
				 if self.maze.layout[i][j][1] == 'X':
					 lines.penup()
					 lines.goto(j * (self.maze.resolution) - 1, i * self.maze.resolution)
					 lines.pendown()
					 lines.forward(self.maze.resolution)
					 lines.penup()
		 turtle.shape('tri')
		 for p in self.particles:
			 p.add_noise(self.maze.dimX,self.maze.dimY)
			 #print(p.x, p.y)
			 turtle.setposition(p.x,p.y)
			 heading = (p.orientation/(2*math.pi))*360
			 turtle.setheading(heading)
			 turtle.color("red")
			 turtle.stamp()
			 #turtle.update()
		 turtle.shape('dot')
		 turtle.color("blue")
		 turtle.setposition(self.particles[self.prWithHeighestW].x, self.particles[self.prWithHeighestW].y)
		 turtle.stamp()
		 turtle.shape('turtle')
		 turtle.color("green")
		 turtle.setposition(_loc[0], _loc[1])
		 headingr = (_loc[2] / (2 * math.pi)) * 360
		 turtle.setheading(headingr)
		 #heading = (self.particles[self.prWithHeighestW].orientation / (2 * math.pi)) * 360
		 #turtle.setheading(heading)
		 turtle.update()











'''Class Particlefilter

#variables
float noise;
Particle[] particles;
Robot robot;
Maze maze;
Particlefilter(Maze maze, float noOfParticles); #constructor
'''