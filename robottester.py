import Robot
import Particlefilter
import Maze
import time
import numpy as np
import math

import Robot
import Particlefilter
import Maze
import time
import numpy as np

layout = 0 #probably an int array
home = 0 #end of maze
particlefilterNoise = 0 #the noise with which the resampling of points is affected
noOfParticles = 1 #number of particles in particle filter
speedOfRobot = 1
rotSpeedOfRotation = 1 #how fast the robot rotates
resolution = 60
fieldSize = 30
T = 1


layout = [['XXOO', 'OXXO', 'OXXO', 'OXXX'],
          ['XOXO', 'OXXO', 'OXXO', 'OXOX'],
          ['XXXO', 'OXXO', 'OXEO', 'OOXX']]

maze2 = np.array([  \
                  [1, 1, 1, 1, 1, 1, 1], \
                  [1, 0, 0, 0, 0, 0, 1], \
                  [1, 0, 1, 1, 1, 1, 1], \
                  [1, 0, 0, 0, 0, 0, 1], \
                  [1, 1, 1, 0, 1, 1, 1], \
                  [1, 0, 0, 0, 0, 0, 1], \
                  [1, 1, 1, 1, 1, 0, 1]])

print maze2

maze = Maze.Maze(layout, resolution, fieldSize)
robot = Robot.Robot(maze, speedOfRobot, rotSpeedOfRotation) 
#particlefilter = Particlefilter.Particlefilter(particlefilterNoise, noOfParticles, maze)
#maze.astar()

robot.measure()
print(robot.measurement)
robot.move([10,0])

robot.measure()
print(robot.measurement)
robot.move([10,0])

robot.measure()
print(robot.measurement)
robot.rotate([10,-math.pi/2])

robot.measure()
print(robot.measurement)
robot.rotate([10,-math.pi/2])

robot.measure()
print(robot.measurement)
robot.move([10,0])

robot.measure()
print(robot.measurement)
robot.rotate([10,math.pi/2])

robot.measure()
print(robot.measurement)
robot.rotate([10])
