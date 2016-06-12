Class Particle

#Variables
int x, y;
float orientation;
float[] measurements;
double weight;

#functions
void calcDistance(Maze Maze);
void updateLocation(Robot robot);
void updateWeight(Robot robot);
void normalizeWeight(float n);