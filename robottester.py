'''Test for robot'''

connected = True
try:
    from gopigo import *
except ImportError:
    connected = False

import sys

servo(0)
print(us_dist(15))
servo(90)
print(us_dist(15))
servo(180)
print(us_dist(15))
