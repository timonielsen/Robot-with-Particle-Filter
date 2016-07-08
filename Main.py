import Robot
import Particlefilter
import Maze
import time
import numpy as np

layout = 0 #probably an int array
home = 0 #end of maze
particlefilterNoise = 0 #the noise with which the resampling of points is affected
noOfParticles = 1000 #number of particles in particle filter
speedOfRobot = 1
rotSpeedOfRotation = 1 #how fast the robot rotates
resolution = 8
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

maze = Maze.Maze(layout, 53, 30)
robot = Robot.Robot(maze, speedOfRobot, rotSpeedOfRotation) 
particlefilter = Particlefilter.Particlefilter(particlefilterNoise, noOfParticles, maze)
#particlefilter.showParticles()

maze.astar()
#particlefilter.showParticles(robot.getSimulatedLocation())
'''
for t in range(T):
    robot.simulateMove(0,5)
    print robot.simulateMeasurements() # it is for simulation of
    particlefilter.updateLocation(0,5)
    particlefilter.compare(robot)
    particlefilter.normalize_weights()
    particlefilter.resample()
#print particlefilter.particles[10].x
    particlefilter.showParticles(robot.getSimulatedLocation())
    '''

#particlefilter.measure()
#particlefilter.compare(robot)
#time.sleep(15)
#maze.printPath()
maze.printLayoutAdvanced(2)
maze.printLayoutAdvanced(3)
#maze.printLayoutAdvancedParticleFilter(particlefilter,5)


'''
Robot robot
Particlefilter particlefilter
Maze maze


#Global variables
int noOfParticles;
int[] layout;
bool running; #should be updated with a click on the button of the robot


#initiliase
maze = new Maze(layout);
robot = New Robot(maze);
particleFilter = New Particlefilter(maze, noOfParticles);

#Run
While(running){
	robot.measure();
	particleFilter.measure();
	particleFilter.compare(robot);
	robot.updateBelief(particlefilter);
	particleFilter.resample();
	robot.findPath();
	robot.move();
	particleFilter.updateLocation(robot);
}
'''