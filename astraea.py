'''
Astraea Spaceflight Simulator - Flynn Bryant
flynn.bryant2001@gmail.com | fbry0688@uni.sydney.edu.au

astraea.py runs the main simulation, sets up the window, then uses the
pyglet.clock.schedule_interval function to call update 60 times per second
(every frame.) Update then calls the simulation and graphical functions.
'''

import pyglet
from data.universe import *
from graphics.scene import *
from graphics.camera import *
from analysis.profiler import *
from analysis.accuracy import *
from mechanics.controls import *
from mechanics.simulation import *

def update(dt, universe, keys, camera, window):
    drawScene(universe, camera, keys, window) #Found in graphics/scene.py
    simulation_cowell(universe, dt) #Found in mechanics/simulation.py
    simulation_controls(universe, camera, window, keys) # Found in mechanics/controls.py
    universe.profile.print_profile(dt) #For testing purposes

window = pyglet.window.Window(1440,846,
caption="Astraea Spaceflight Simulator")
pyglet.clock.schedule_interval(update, 1/60,
    universe = Universe(focus='Jupiter',profile=False,rate=60),
    keys = pyglet.window.key.KeyStateHandler(),
    camera = Camera(window), window = window)
pyglet.app.run()
