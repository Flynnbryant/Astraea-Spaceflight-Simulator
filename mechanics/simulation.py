''' simulation.py
Each frame of the simulation executes the following steps:
1. Executes any nodes if applicable (see analysis/nodes.py for information)
2. Iterates through every entity in the universe:
    a. Iterates through every body (entities with mass):
        i. Checks for collisions
        ii. Accelerates the entity by the gravitational attraction
3. Changes the position of each object based on its velocity
'''

from mechanics.entities import *
from analysis.accuracy import *
import numpy as np
import pyglet

def simulation_timestep(universe, dt):
    universe.timestep = universe.usertime*dt
    if universe.nodes[0].time < universe.time:
        universe.nodes[0].run(universe)
        nodes.pop(0)
    for entity in universe.entities:
        for body in universe.bodies:
            if body is not entity:
                distVec = (body.pos - entity.pos)
                if np.linalg.norm(distVec) < body.radius:
                    entity.remove(universe)
                entity.vel += universe.timestep*body.SGP*distVec/np.linalg.norm(distVec)**3
    universe.profile.add('gravity')

    universe.entities[0].pos += universe.entities[0].vel * universe.timestep
    for entity in universe.entities[1:]:
        entity.pos += entity.vel * universe.timestep
        entity.orbital_elements()
    universe.time += universe.timestep
    universe.profile.add('elements')

    #prioritise wobbling and focus objects
    universe.entities[(universe.tracecount%(len(universe.entities)-1))+1].calculate_trace()
    universe.tracecount += 1
    universe.profile.add('trace')
