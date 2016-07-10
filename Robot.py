import Particle

class Robot:
    def __init__(self, _maze, _speed, _rotationSpeed): #give it a maze as input!
        
        self.maze = _maze
        ###Variables for robot###
        self.x = 30.0 #location, initiliased to zero as the robot initialy has no clue where it is
        self.y = 30.0
        self.orientation = 0 #[0, 2PI]
        self.pr = Particle.Particle(self.x, self.y, self.orientation) # since we don't have any data for robot, for simulation
        # robot is defined as particle
        self.pr.set_noise(5.0, 1.0, 1.0) # these are for movement and sense distribution
        
        self.speed = _speed; #Speed with which the robot moves forwards
        self.rotationSpeed = _rotationSpeed; #
        
        self.movement = [0,0] # stores the last movement [length moved, rotation]
        self.measurement = [0.0,0.0,0.0] #we can always re evaluate number of points here. DO NOT MAKE ANY HARD CODED LOOPS.
        
        #The following are hard coded values found from measurements of the precision of robot movement. Length of arrays to be determined
        self.moveVar = [0,0,0,0,0] #variance in distance actually moved
        self.moveMean = [0,0,0,0,0]
        self.moveOrientVar = [0,0,0,0,0] #variance in orientation when moving forward
        self.moveOrientMean = [0,0,0,0,0]
        self.orientVar = [0,0,0,0,0] #variance in orientation when rotating
        self.orientMean = [0,0,0,0,0]
        self.measurementVar = [0,0,0,0,0] #variance in orientation when rotating
        self.measurementMean = [0,0,0,0,0]
        self.measurementLimHigh = 1e10 #limit for measurement. Set to some desired value
        self.measurementLimLow = 0

    
    def move(self, _distance):
        """Moves the robot. postive values=forward, negative values=backward"""
        return 0

    def rotate(self, _angle):
        """Rotate robot. Be aware of sign of angle. We need to figure out if CW is positive"""
        if connected:
            fullCircle = 32 #units
            partsOfCircle = math.pi*2/_angle #how big a part of a full circle is rotated. eg 90 degrees = 4

            units = int(round(fullCircle/partsOfCircle))
            set_speed(80)  #DO NOT CHANGS UNLESS NEW TESTS ARE MADE WITH ROBOT TO CHECK HOW MANY UNITS GO TO FULL CIRCLE
            enc_tgt(1,1,units)
            right_rot() #Choose whether it should be clockwise or counterclockwise

        return 0

    def measure(self): 
        """Updates measurement[] with a series of measurements."""
        self.measurement = self.simulateMeasurements()
        return self.measurement

    def updateBelief(self, _particleFilter): #updates x, y and rotation
        """updates x, y and rotation"""
        return 0

    def findPath(self):
        """Finds the shortest path out of the maze. 
        No need to have maze as input as the maze is a variable for the robot"""
        return 0

    def rotateServo(self):
        """this function might just be moved to be a part of the measure() function.""" 
        return 0

    def simulateMeasurements(self):
        self.pr.calcDistance(self.maze)
        return self.pr.measurements

    def simulateMove(self,_angle,_distance):
        self.pr.move(_angle,_distance,self.maze)
        return 0

    def getSimulatedLocation(self):
        return self.pr.getStateofParticle()





'''
#Variables
x, y; #int
float orientation;
int speed, rotationSpeed;
int[2] movement; #array of distance forward as well as rotation. 
float[] measurement; #array of measurements. Most likely of size 5
Maze maze; #robot stores the maze in it's own memory

float[] moveVar, moveMean, moveRotVar, moveRotMean; #normal Distribution values for moving forward/backward. Array so values for different speeds can be stored. These values are constants that we hard code. moveRotVar is for the expected rotation while moving forward/backward
float[] rotVar, rotMean; #Normal distribution for rotation
float[] measurementVar, measurementMean; #Normal distribution for measurement

float measurementLimHigh,measurementLimLow; #hard coded limits for measurements

#Functions
void move(float distance); #postive values=forward, negative values=backward
void rotate(float angle); #negative or positive values
void measure(); #Updates measurement[] with a series of measurements.
void updateBelief(Particlefilter particleFilter); #updates x, y and rotation
void findPath() #Finds the shortest path out of the maze. No need to have maze as input as the maze is a variable for the robot
void rotateServo() # this function might just be moved to be a part of the measure() function.
'''