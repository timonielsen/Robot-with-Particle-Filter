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
resolution = 40
fieldSize = 30
T = 40

layout = [['XXOO', 'OXXO', 'OXXX'],
                  ['XOXO', 'OXXO', 'OXOX'],
                  ['XXXO', 'OXXO', 'OOEX']]

maze2 = np.array([  \
                  [1, 1, 1, 1, 1, 1, 1], \
                  [1, 0, 0, 0, 0, 0, 1], \
                  [1, 0, 1, 1, 1, 1, 1], \
                  [1, 0, 0, 0, 0, 0, 1], \
                  [1, 1, 1, 1, 1, 0, 1], \
                  [1, 0, 0, 0, 0, 0, 1], \
                  [1, 1, 1, 1, 1, 0, 1]])

print maze2

maze = Maze.Maze(layout, resolution, fieldSize)
#print maze.fullLayout
robot = Robot.Robot(maze, speedOfRobot, rotSpeedOfRotation) 
particlefilter = Particlefilter.Particlefilter(particlefilterNoise, noOfParticles, maze)
#particlefilter.showParticles()

#particlefilter.showParticles(robot.getSimulatedLocation())

for t in range(T):
  '''Perform measurements'''
  robot.measure()
  particlefilter.compare(robot)
  particlefilter.normalize_weights()

  particlefilter.resample()
  robot.updateBelief(particlefilter.bestParticle.x, particlefilter.bestParticle.y, particlefilter.bestParticle.orientation)

  maze.update((int(robot.pr.y),int(robot.pr.x)))
  maze.astar()

  robot.calculateMovementOnPath(20,maze)
  #maze.printLayoutAdvancedRobot(robot,6)
  particlefilter.showParticles(robot.getSimulatedLocation())

  robot.move()
  particlefilter.updateLocation(robot.movement[1], robot.movement[0])
  robot.reset()
  time.sleep(0)
  

  '''
    robot.simulateMove(0,5)
    robot.simulateMeasurements() # it is for simulation of
    # print robot.pr.orientation
    #particlefilter.showParticles(robot.getSimulatedLocation())
    # print("BP1")
    # print particlefilter.particles[5].x
    particlefilter.updateLocation(0.0,5.0)
    # print("BP2")
    # print particlefilter.particles[5].x
    #particlefilter.showParticles(robot.getSimulatedLocation())
    particlefilter.compare(robot)
    particlefilter.normalize_weights()
    particlefilter.resample()
#print particlefilter.particles[10].x
    particlefilter.showParticles(robot.getSimulatedLocation())
    #time.sleep(1)
    '''


'''
    #time.sleep(15)
i = 0
while i < 20:
  #print("START ROUND")
  #print(i)
  robot.measure()
  maze.update((int(robot.y),int(robot.x)))
  maze.astar()
  #print("now it comes")
  

  #maze.printLayoutAdvanced(2)
  maze.printLayoutAdvancedRobot(robot,6)
  # maze.printPath()

  robot.calculateMovementOnPath(8,maze)
  #robot.movement= [0,0]
  #print("robotLoc")
  print(robot.measurement)
  print(int(robot.x), int(robot.y),robot.orientation)
  #print("movement")
  #print(robot.movement)
  robot.move()
  #print("robotLoc")
  #print(int(robot.x), int(robot.y),robot.orientation)
  robot.pr.rayTracedNodes ={}

  i += 1

print T
'''



#particlefilter.measure()
#particlefilter.compare(robot)
#maze.printPath()
#maze.printLayoutAdvancedParticleFilter(particlefilter,4)
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