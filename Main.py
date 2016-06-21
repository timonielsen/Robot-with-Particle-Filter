import Robot
import Particlefilter
import Maze

layout = 0 #probably an int array
home = 0 #end of maze
particlefilterNoise = 0 #the noise with which the resampling of points is affected
noOfParticles = 100 #number of particles in particle filter
speedOfRobot = 1
rotSpeedOfRotation = 1 #how fast the robot rotates
resolution = 8
fieldSize = 30

layout = [['XXOO', 'OXXO', 'OXXO', 'OXXX'],
          ['XOXO', 'OXXO', 'OXXO', 'OXOX'],
          ['XXXO', 'OXXO', 'OXEO', 'OOXX']]

maze = Maze.Maze(layout, 10, 30)
robot = Robot.Robot(maze, speedOfRobot, rotSpeedOfRotation) 
particlefilter = Particlefilter.Particlefilter(particlefilterNoise, noOfParticles, maze)





maze.astar()
maze.printLayoutAdvanced(3)
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