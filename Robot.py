Class Robot

#Variables
int x, y;
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