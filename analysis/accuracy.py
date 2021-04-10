'''accuracy.py
Used to compare the position of the moon (Luna) to the JPL value after one
month. Luna is chosen for this because moons are affected more by innacuracies
in timestep (as each timestep is a higher fraction of their orbit) and Luna's
large orbit is affected by the Sun more than other closer moons. Additionally,
I am latter planning to calculate solar eclipses, and so measuring my progress
by Luna's error is useful to work towards that goal.

lunar_accuracy is currently not called anywhere in the code.
'''
import numpy as np
from analysis.profiler import *
from mechanics.simulation import *

def lunar_accuracy(dt, universe, keys, camera, window):
    simulation_timestep(universe, dt)
    universe.profile.print_profile(dt)
    #print(universe.time)
    #print((universe.time-1609419600)/16120980)
    if universe.time > 1612098000:
        ### Need to get more accurate value
        luna_pos = np.array([
        -1.001230325085023E+011,
        1.103636458084704E+011,
        4.449697438944131E+07]) # Position from JPL after one month.
        print(universe.entities[4].name + ' error: ' + str(round(np.linalg.norm(universe.entities[4].pos - luna_pos)/1000)) + 'km, radius = ' + str(round(universe.entities[4].radius/1000)))
        quit()
