''' simulation.py
Runs the methods of numerical integration to calculate new positions and
velocities for each body and vessel. Currently the cowell method is in use.
This is called each frame from astraea.py
'''


from mechanics.entities import *
from analysis.accuracy import *
import numpy as np
import pyglet

def simulation_cowell(universe, dt):
    universe.usertime = min(universe.usertime,43200)
    universe.timestep = universe.usertime*dt
    universe.time += universe.timestep
    if universe.nodes[0].time < universe.time:
        universe.nodes[0].run(universe)

    for body in universe.bodies:
        for target in universe.bodies:
            if body is not target:
                distVec = (target.pos - body.pos)
                body.vel += universe.timestep*target.SGP*distVec/np.linalg.norm(distVec)**3

    universe.entities[0].pos += universe.entities[0].vel * universe.timestep
    for body in universe.bodies[1:]:
        body.pos += body.vel * universe.timestep
        body.orbital_elements()

    for vessel in universe.vessels:
        for body in universe.bodies:
            distVec = (body.pos - vessel.pos)
            vessel.vel += universe.timestep*body.SGP*distVec/np.linalg.norm(distVec)**3
        vessel.pos += vessel.vel * universe.timestep
        vessel.orbital_elements()
        vessel.calculate_trace()
        primarydistance = np.linalg.norm(vessel.pos - vessel.primary.pos)
        if primarydistance < vessel.primary.radius:
            vessel.remove(universe)
        elif primarydistance > vessel.primary.hill:
            vessel.primary = vessel.primary.primary
        else:
            for sibling in vessel.primary.satellites:
                if np.linalg.norm(vessel.pos - sibling.pos) < sibling.hill:
                    vessel.primary = sibling

    universe.bodies[(universe.tracecount%(len(universe.bodies)-1))+1].calculate_trace()
    universe.tracecount += 1
    universe.profile.add('gravity')

def simulation_encke(universe, dt):
    '''
    Work in progress to move the simulation to the Encke method
    '''
    universe.timestep = min(universe.usertime*dt, 31104000)
    universe.time += universe.timestep
    universe.tracecount += 1

    for body in universe.bodies[1:]:
        body.pos = elements_to_state(body, botched_anomaly(body, universe.time))
        for sibling in body.primary.satellites:
            if sibling is not body:
                distVec = (sibling.pos - body.pos)
                body.pvel += universe.timestep*sibling.barySGP*distVec/np.linalg.norm(distVec)**3
        #body.ppos += body.pvel * universe.timestep
        #body.pos += body.primary.pos + body.ppos
        body.pos += body.primary.pos

    for vessel in universe.vessels:
        for body in universe.bodies:
            distVec = (body.pos - vessel.pos)
            vessel.vel += universe.timestep*body.SGP*distVec/np.linalg.norm(distVec)**3
        vessel.pos += vessel.vel * universe.timestep
        state_to_elements(vessel)
        vessel.calculate_trace()
        primarydistance = np.linalg.norm(vessel.pos - vessel.primary.pos)
        if primarydistance < vessel.primary.radius:
            vessel.remove(universe)
        elif primarydistance > vessel.primary.hill:
            vessel.primary = vessel.primary.primary
        else:
            for sibling in vessel.primary.satellites:
                if np.linalg.norm(vessel.pos - sibling.pos) < sibling.hill:
                    vessel.primary = sibling

    rectification_body = universe.bodies[(universe.tracecount%(len(universe.bodies)-1))+1]
    rectification_body.calculate_trace()
    state_to_elements(rectification_body)
    rectification_body.epoch = universe.time
    rectification_body.ppos = 0
    rectification_body.pvel = 0
    rectification_body.epoch_anomaly = rectification_body.mean_anomaly

    universe.profile.add('simulation')
    if universe.nodes[0].time < universe.time:
        universe.nodes[0].run(universe)

def state_to_elements(entity):
    rel_pos = entity.pos - entity.primary.pos
    rel_vel = entity.vel - entity.primary.vel
    entity.eccentricity_vec = ((np.linalg.norm(rel_vel)**2)/entity.primary.SGP - 1/np.linalg.norm(rel_pos))*rel_pos - rel_vel*(np.dot(rel_pos, rel_vel)/entity.primary.SGP)
    entity.eccentricity = np.linalg.norm(entity.eccentricity_vec)
    entity.semi_major_axis = -0.5*entity.primary.SGP/(0.5*(np.linalg.norm(rel_vel))**2 - entity.primary.SGP/np.linalg.norm(rel_pos))
    entity.semi_minor_axis = entity.semi_major_axis*np.sqrt(1-entity.eccentricity**2)
    entity.periapsis = entity.semi_major_axis*(1-entity.eccentricity)
    entity.plane_vec = np.cross(rel_pos,rel_vel)
    entity.inclination = np.arccos(entity.plane_vec[2]/np.linalg.norm(entity.plane_vec))
    entity.ascending_node = np.cross(np.array([0,0,1]),np.cross(rel_pos, rel_vel))
    entity.long_ascending = np.arccos(entity.ascending_node[0]/np.linalg.norm(entity.ascending_node))
    entity.arg_periapsis = np.arccos(np.dot(entity.ascending_node, entity.eccentricity_vec)/(np.linalg.norm(entity.ascending_node)*np.linalg.norm(entity.eccentricity_vec)))
    if entity.eccentricity_vec[2] <0:
        entity.arg_periapsis = 2*np.pi - entity.arg_periapsis
    if entity.ascending_node[1] < 0:
        entity.long_ascending = 2*np.pi - entity.long_ascending

def true_anomaly(entity, time):
    ''' mean -> true '''
    mean_anomaly = entity.epoch_anomaly + (time-entity.epoch)*(entity.primary.SGP/entity.semi_major_axis**3)**0.5
    E0 = np.pi * np.sign(mean_anomaly)
    ###
    return 2 * np.arctan(np.sqrt((1+entity.eccentricity)/(1-entity.eccentricity))*np.tan(eccentric_anomaly*0.5))

def elements_to_state(entity, anomaly):
    x_translated = entity.semi_major_axis * np.cos(anomaly) - entity.semi_major_axis + entity.periapsis
    y_translated = entity.semi_minor_axis * np.sin(anomaly)
    x_periapsis_rotation = x_translated * np.cos(entity.arg_periapsis) - y_translated * np.sin(entity.arg_periapsis)
    y_periapsis_rotation = x_translated * np.sin(entity.arg_periapsis) + y_translated * np.cos(entity.arg_periapsis)
    y_inclination_rotation = y_periapsis_rotation * np.cos(entity.inclination)
    x_longitude_rotation = x_periapsis_rotation * np.cos(entity.long_ascending) - y_inclination_rotation * np.sin(entity.long_ascending)
    y_longitude_rotation = x_periapsis_rotation * np.sin(entity.long_ascending) + y_inclination_rotation * np.cos(entity.long_ascending)
    return [x_longitude_rotation, y_longitude_rotation, y_periapsis_rotation * np.sin(entity.inclination)]
