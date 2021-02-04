''' accuracy.py
Used to compare the position of the moon (Luna) to the JPL value after one
month. Luna is chosen for this because moons are affected more by innacuracies
in timestep (as each timestep is a higher fraction of their orbit) and Luna's
large orbit is affected by the Sun more than other closer moons. Additionally,
I am latter planning to calculate solar eclipses, and so measuring my progress
by Luna's error is useful to work towards that goal.

lunar_accuracy is currently not called anywhere in the code.
'''
'''
import numpy as np

def lunar_accuracy(luna):
    luna_pos = np.array([
    -1.001230325085023E+011,
    1.103636458084704E+011,
    4.449697438944131E+07]) # Position from JPL after one month.
    print(luna.name + ' error: ' + str(round(np.linalg.norm(luna.pos - luna_pos)/1000)) + 'km, radius = ' + str(round(luna.radius/1000)))
    quit()

'''
'''


import pyglet
from Astraea-Spaceflight-Simulator.data.universe import *
#from graphics.scene import *
#from graphics.camera import *
from analysis.profiler import *
#from mechanics.controls import *
from mechanics.simulation import *

universe = Universe('Earth')
dt = 0.03
while True:
    simulation_timestep(universe, dt)
    universe.profile.print_profile(dt)
    if universe.time > 1612098000: #One month after simulation start
        lunar_accuracy(universe.entities[4])

'''
'''
def update(dt, universe, keys, camera, window):
    drawScene(universe, camera, keys, window)
    simulation_timestep(universe, dt)
    simulation_controls(universe, camera, window, keys)
    universe.profile.print_profile(dt)

window = pyglet.window.Window(1440,846,
caption="Astraea Spaceflight Simulator")
pyglet.clock.schedule_interval(update, 1/60,
    universe = Universe('Earth'),
    keys = pyglet.window.key.KeyStateHandler(),
    camera = Camera(window), window = window)
pyglet.app.run()
while True:
'''
