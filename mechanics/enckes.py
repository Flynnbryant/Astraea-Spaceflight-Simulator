from mechanics.entities import *
from analysis.accuracy import *
import numpy as np
import pyglet

def simulation_encke(universe, dt):
    universe.timestep = universe.usertime*dt
    if universe.nodes[0].time < universe.time:
        universe.nodes[0].run(universe)
        nodes.pop(0)

    for entity in universe.entities[1:]:

        #calculate pertubations from siblings
        if entity.primary.primary:
            for body in entity.primary.satellites:
                if body is not entity:
                    distVec = (body.pos - entity.pos)
                    if np.linalg.norm(distVec) < body.radius:
                        entity.remove(universe)
                    entity.vel += universe.timestep*body.SGP*distVec/np.linalg.norm(distVec)**3

        #calculate perturbations from barycentres
        for barycentre in universe.barycentres:
            if barycentre is not entity:
                distVec = (barycentre.pos - entity.pos)
                entity.vel += universe.timestep*barycentre.B_SGP*distVec/np.linalg.norm(distVec)**3

        #Somewhere above, the affect of the planet's moons must be accounted for.
        #The barycentre's orbit must be different from the planet's orbit.
        
        #calculate cartesian position from orbit and add pertubations
        #recalculate orbital elements from state vectors
        #check for collision with parent
        pass


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