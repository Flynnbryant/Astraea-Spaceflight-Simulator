'''
Astraea Spaceflight Simulator - by Flynn Bryant
flynn.bryant2001@gmail.com
fbry0688@uni.sydney.edu.au
Project start: Jan 27th 2021
Current version: 0.1.0 (Feb 5th 2021)

Some sections of this project were first written in a more basic and less
efficient form for previous orbital mechanics simulators I have written, such
as 'orbit', presented at the University of Sydney Coding Fest 2020.

astraea.py runs the main simulation, sets up the window, then uses the
pyglet.clock.schedule_interval function to call update 60 times per second
(every frame.) Update then calls the simulation and graphical functions.
'''

import pyglet
from data.universe import *
from graphics.scene import *
from graphics.camera import *
from analysis.profiler import *
from mechanics.controls import *
from mechanics.simulation import *

def update(dt, universe, keys, camera, window):
    drawScene(universe, camera, keys, window)
    simulation_timestep(universe, dt)
    simulation_controls(universe, camera, window, keys)
    universe.profile.print_profile(dt)

window = pyglet.window.Window(1440,846,
caption="Astraea Spaceflight Simulator")
pyglet.clock.schedule_interval(update, 1/60,
    universe = Universe('Mercury'),
    keys = pyglet.window.key.KeyStateHandler(),
    camera = Camera(window), window = window)
pyglet.app.run()
