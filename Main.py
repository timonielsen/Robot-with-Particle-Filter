import Robot
import Particlefilter
import Particle
import Maze
import time
import numpy as np

layout = 0 #probably an int array
home = 0 #end of maze
particlefilterNoise = 0 #the noise with which the resampling of points is affected
noOfParticles = 1 #number of particles in particle filter
speedOfRobot = 1
rotSpeedOfRotation = 1 #how fast the robot rotates
resolution = 30
fieldSize = 30.0
T =2

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
sleepTime = 0

 #change to some random value

for t in range(T):
  particlefilter.particles[0] = Particle.Particle(robot.x, robot.y,robot.orientation)
  #movement = [5,0]
  maze.printLayoutAdvanced(2)
  maze.printLayoutAdvancedParticleFilter(particlefilter,4)
  maze.printLayoutAdvancedParticleFilter(particlefilter,5)
  '''measure'''
  robot.measure()
  particlefilter.compare(robot)
  print("")
  print(particlefilter.particles[0].measurements)
  print(robot.measurement)
  print("")
  particlefilter.normalize_weights()
  
  print(particlefilter.particles[0].y, particlefilter.particles[0].x, particlefilter.particles[0].orientation)
  print(robot.y, robot.x, robot.orientation)


  '''find path'''
  maze.update((int(robot.x),int(robot.y)))
  maze.astar()

  '''resample particles'''
  particlefilter.resample()
  particlefilter.showParticles(robot.getLocation())
  #print("Resampled")
  time.sleep(sleepTime)
  particlefilter.showParticles(robot.getLocation())


  '''calculate how to move on path and move'''
  robot.calculateMovementOnPath(5,maze)
  print(robot.movement)
  #print(robot.movement)
  #print(robot.x, robot.y, robot.orientation)
  #robot.movement = movement
  robot.move()
  particlefilter.showParticles(robot.getLocation())
  #print("Robot Moved")
  time.sleep(sleepTime)
  #print(robot.x, robot.y, robot.orientation)

  #print(particlefilter.particles[0].x,particlefilter.particles[0].y,particlefilter.particles[0].orientation)
  particlefilter.updateLocation(robot.movement[1],robot.movement[0])
  particlefilter.showParticles(robot.getLocation())
  particlefilter.reset_particles()
  #print("Particles moved")
  #print(particlefilter.particles[0].x,particlefilter.particles[0].y,particlefilter.particles[0].orientation)
  time.sleep(sleepTime)
  #maze.printLayoutAdvancedParticleFilter(particlefilter,5)


  print("################################################")
  print("################################################")
  print("################################################")



  


  #robot.simulateMeasurements() # it is for simulation of
  # print robot.pr.orientation
  
  # print("BP1")
  # print particlefilter.particles[5].x

  # print("BP2")
  # print particlefilter.particles[5].x
  #particlefilter.showParticles(robot.getSimulatedLocation())
  ##particlefilter.compare(robot)
  ##particlefilter.normalize_weights()
  time.sleep(1)
  #print particlefilter.particles[10].x


    #time.sleep(15)


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